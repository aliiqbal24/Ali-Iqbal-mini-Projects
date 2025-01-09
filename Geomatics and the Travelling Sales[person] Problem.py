import scipy.io as io
import numpy as np
import matplotlib.pyplot as plt


# this section uses the choice generated in the menu to decide which function will be called next
def main():
    file = open('tspAbout.txt','r')
    print(file.read())
    file.close()
    print()
    tsp = io.loadmat('tspData.mat', squeeze_me=True)
    tsp = np.ndarray.tolist(tsp['tsp'])
    Choice = menu()
    while Choice != 0:
        if Choice == 1:
            tspPrint(tsp)
        elif Choice == 2:
            tsp = tspLimit(tsp)
        elif Choice == 3:
            tspPlot(tsp)
        Choice = menu()

# this section gets the user to input 1,2 or 3 and it sets the choice value, which is used in main 
def menu():
    print("MAIN MENU")
    print("0. Exit Program")
    print("1. Print Database")
    print("2. Limit Dimension")
    print("3. Plot One Tour")
    print()
    Choice = int(input("Choice(0-3)? "))
    while not ((0 <=Choice<= 3)):
        Choice = int(input("Choice(0-3)? "))
    return Choice

#this section reads tsp and gives it some values based of its np.array
def tspPrint(tsp):
    print()
    print("NUM  FILE NAME  EDGE TYPE  DIMENSION  COMMENT")
    for k in range(1,len(tsp)):
        Name= tsp[k][0]
        Edge= tsp[k][5]
        Dimension= tsp[k][3]
        Comment= tsp[k][2]
        print("%3d  %-9.9s  %-9.9s  %9d  %s"
              % (k,Name,Dimension,Edge,Comment))
        
# this section prints the maximum and minimum dimensions located in tspE and gets the user to input
#a limit between the max and min, there is a while lopp to make sure that the program stays running 
# until a valid input is input, the the words in the tsp tuple are saved for later. the function 
# removes all the values in tsp that are greater than the limt, puts the header back at the top
# and returns the new value which is taken to the main function
def tspLimit(tsp):
    minD, maxD = tspE(tsp)
    print ("Min Dimension:",minD)
    print ("Max Dimension:",maxD)
    lim = int(input("Enter limit value between max and min dimension "))
    while lim > maxD or lim < minD: 
        lim = int(input("invalid input"))
    tspWord = tsp[0]
    tsp = [i for i in tsp[1:] if i[3] <= lim]
    tsp.insert(0, tspWord)
    return tsp

# this section gets all the dimension values of the tsp tuple as well as finding the maximum and
#minimum values which are used in the tsp limit function
def tspE(tsp):
    tspD= [i[3] for i in tsp[1:]]
    minD= min(tspD)
    maxD= max(tspD)
    return minD, maxD

#this section takes the user input of EUC_2D and pushes it forward to the plotEUC2D function which 
# which plot it, if the EUC_2D input is invalid, it will keep prompting the user to enter a valid 
#input
def tspPlot(tsp):
    print()
    print()
    Num = int(input("Number (EUC_2D)? "))
    while Num < 0 or Num > len(tsp):
        Num = int(input("Invalid input, Number (EUC_2D)?"))
    edge = tsp[Num][5]
    tsp1 = tsp[Num]
    if edge == 'EUC_2D':
        plotEuc2D(tsp1[10],tsp1[2],tsp1[0])
        print("See tspPlot.png")
    else:
        print("Invalid (%s)!!!" % edge)    


def plotEuc2D(coord,Comment,Name):
    plt.title(Comment)
    x1 = coord[:,0]
    y1 = coord[:,1]
    x2 = [coord[0,0],coord[-1,0]]
    y2 = [coord[0,1],coord[-1,1]]
    plt.xlabel("x coordinate")
    plt.ylabel("y coordinate")
    plt.legend("[name]")
    plt.plot(x1,y1,marker = '.', label = Name)
    plt.plot(x2,y2, c = "r")
    plt.legend()
    plt.show()


main()



