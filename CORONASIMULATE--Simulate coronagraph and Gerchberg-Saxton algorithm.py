import matplotlib.pyplot as plt
import numpy as np


def main():
    im = loadImage('300_26a_big-vlt-s.jpg')
    (im,Dphi) = opticalSystem(im,300)
    images = gerchbergSaxton(im,10,Dphi,mask)
    saveFrames(images)

#  this function loads an image file and prepares it for further processing
def loadImage(name):
    im = plt.imread(name)/255
    if len(im.shape) > 2:
        im = (im[:,:,0]+im[:,:,1]+im[:,:,2])/3
    im[im < 0] = 0
    im[im > 1] = 1
    return im

# Creates an obstruction in the center of the image.
# Applies transformations to image
def opticalSystem(im,width):
    im = occultCircle(im,width)
    (IMa,IMp) = dft2(im)
    rng = np.random.default_rng(12345)
    imR = rng.random(im.shape)
    (_,Dphi) = dft2(imR)
    im = idft2(IMa,IMp-Dphi,mask)
    return (im,Dphi,mask)

# this function places a square-shaped obstruction at the center of the image.
def occultCircle(im,width):
    x,y = im.shape[1]//2, im.shape[0]//2
    half_w = width // 2
    x_c, y_c= np.ogrid[:im.shape[0], :im.shape[1]]
    mask = np.full_like(im,False)
    c = (y_c-y)**2+(x_c-x)**2 <= half_w**2
    im[c] = 0
    mask[c] = True
    return im, mask

# (IMa,IMp) = dft2(im) returns the amplitude, IMa, and phase, IMp, of the
# 2D discrete Fourier transform of a grayscale image, im. The image, a 2D
# array, must have entries between 0 and 1. The phase is in radians.

# this function finds details in the image
def dft2(im):
    IM = np.fft.rfft2(im)
    IMa = np.abs(IM)
    IMp = np.angle(IM)
    return (IMa,IMp)

# im = idft2(IMa,IMp) returns a grayscale image, im, with entries between
# 0 and 1 that is the inverse 2D discrete Fourier transform (DFT) of a 2D
# DFT specified by its amplitude, IMa, and phase, IMp, in radians.


# this function corrects the image
def idft2(IMa,IMp):
    IM = IMa*(np.cos(IMp)+1j*np.sin(IMp))
    im = np.fft.irfft2(IM)
    im[im < 0] = 0
    im[im > 1] = 1
    return im


# improves photo with algorithm
def gerchbergSaxton(im,maxIters,Dphi,mask):
    (IMa,IMp) = dft2(im)
    images = []
    errors = []
    for k in range(maxIters+1):
        print("Iteration %d of %d" % (k,maxIters))
        beta = k/maxIters
        d = (1-beta)*IMp + beta *(IMp + Dphi) # Linear interpolation calculation
        im = idft2(IMa,d)
        images.append(im)
        error = occultError(im,mask)
        errors.append(error)
    return images,errors

# this function saves improved versions of the photo
def saveFrames(images,errors):
    shape = (images[0].shape[0],images[0].shape[1],3)
    image = np.zeros(shape,images[0].dtype)
    maxIters = len(images)-1
    maxErrors = max(errors)
    for k in range(maxIters+1):
        image[:,:,0] = images[k] #Red
        image[:,:,1] = images[k] # Green
        image[:,:,2] = images[k] #Blue
        plt.plot(range(k+1), errors[:k+1], color='r')
        plt.imshow(image, extent=(0, maxIters, 0, maxErrors))
        plt.gca().set_aspect(maxIters/maxErrors)
        plt.title('Coronagraph Simulation')
        plt.xlabel('Iteration')
        plt.ylabel('Sum Square Error')
        plt.savefig('coronagraph'+str(k)+'.png')
        plt.show()

def occultError(im,mask):
    i = np.where(mask)
    z = im[i]
    error = np.sum(z**2)
    return error

main()
