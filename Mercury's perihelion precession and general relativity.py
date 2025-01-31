# Mercury's perihelion


import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import csv
def main():
    data = loaddata('horizons_results')
    data = locate(data) # Perihelia
    data = select(data,50,('Jan','Feb','Mar'))
    data = refine(data,'horizons_results')
    makeplot(data,'horizons_results')
    savedata(data,'horizons_results')
    
#End of main function
## Initates all auxilery functions
#

def loaddata(filename):
    file = open(filename+".txt","r")
    lines = file.readlines()
    file.close()
    noSOE = True
    num = 0
    data = []
    for line in lines:
        if noSOE:
            if line.rstrip() =="$$SOE":
                noSOE = False
        elif line.rstrip() !="$$EOE":
            num = num+1
            if num % 10000 == 0:
                print(filename,":",num,"line(s)")
            datum = str2dict(num,line)
            data.append(datum)
        else:
            break  #for
    if noSOE:
        print(filename,": no $$SOE line")
    else:
        print(filename,":",num,"line(s)")
    return data
#End of loaddata function
## Opens the data file, iniates the string to dictionary function
#Uses the string to dictionary function to append the origional data


def str2dict(num,line):
    s  = line.split(',')
    numdate = float(s[0])
    f = str((s[1]))
    strdate = (f[6:17])
    coord = (float(s[2]),float(s[3]),float(s[4]))
    #yaph = 6.98169e7 # Aphelion (km)
   #yprh = 4.60012e7 # Perihelion (km)
   #days = 87.9691 # Orbit period (d)
   # sine = (np.cos(2*np.pi*numdate/days)+1)/2
    return {'numdate':numdate,'strdate':strdate,
            'coord':coord}
#End of string to dictionary function
## Creates a dictionary which defines the number date, the date in a string,
# and the coordinates for each respective date


def locate(data1):
    dist = [] # Vector lengths
    for datum in data1:
        coord = np.array(datum['coord'])
        dot = np.dot(coord,coord)
        dist.append(np.sqrt(dot))
    data2 = []
    for k in range(1,len(dist)-1):
        if  dist[k] < dist[k-1] and dist[k]< dist[k+1]:
            data2.append(data1[k])
    return data2

#End of locating function
## The locating function locates where each perihelion occurs in the data.
#Then, returns the new data with the perihelion located

def select(data,ystep,month):
    v = []
    for i in range (0, len(data)):
        p = data[i]['strdate']
        c = p.split('-')
        y = int(c[0])
        mV = str(c[1])
        if y % ystep ==0 and mV in month:
            v.append(data[i])
    #if len(data) > 10:
    #data = data[0:10]
    return v
          
    
def makeplot(data,filename):
    (numdate,strdate,arcsec) = precess(data)
    plt.plot(numdate,arcsec,'bo')
    plt.xticks(numdate,strdate,rotation=45)
    add2plot(numdate,arcsec)
    plt.savefig(filename+'.png',bbox_inches='tight')
    plt.show()
    
    

def precess(data):
    numdate = []
    strdate = []
    arcsec = []
    v = np.array(data[0]["coord"])   # Reference (3D)
    for datum in data:
        u = np.array(datum["coord"])     # Perihelion (3D)
        ratio = np.dot(u,v)/np.sqrt(np.dot(u,u)*np.dot(v,v))
        if np.abs(ratio) <= 1:
            angle = 3600*np.degrees(np.arccos(ratio))
            numdate.append(datum['numdate'])
            strdate.append(datum['strdate'])
            arcsec.append(angle)
    return (numdate,strdate,arcsec)



def add2plot(numdate,actual):
    r = stats.linregress(numdate,actual)
    bestfit = []
    for k in range(len(numdate)):
        bestfit.append(r[0]*numdate[k]+r[1])
    plt.plot(numdate,bestfit,'b-')
    slope = str(round(r[0]*365.25*100,2))
    plt.legend(["Actual data", "Best fit line"])
    plt.title('Slope of Best Fit Line: ' + slope + ' arcsec/cent')
    plt.xlabel("Perihelion date")
    plt.ylabel("Precession (arcsec)")
    
    
def savedata(data,filename):
    newFile = open(filename + '.csv', 'w', newline = '')
    writing = csv.writer(newFile)
    writing.writerow(['NUMDATE', 'STRDATE', 'X-COORD','Y-COORD', 'Z-COORD'])
    for element in data:
        writing.writerow([element['numdate'], element['strdate'], element['coord'][0], element['coord'][1],element['coord'][2]])
    newFile.close()
#End of save data function
##The save data function creates a new csv file, writes the new file including
#each of the values inside our refined data
    
def refine(data,filename):
    DATA = []
    for element in data:
        Data = loaddata(filename + "_" + element['strdate'])
        Data = locate(Data)
        DATA.append(Data[0])
    return DATA

main()
