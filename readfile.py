import numpy as np
import re 

def read():
#fname = input("Please give the name of the file: ")
    f = open("AISearchfile012.txt", "r")

    lines = []
    #Reading lines while ingoring blank lines and white spaces in between and also not inputing \n in the list
    for line in f.readlines():
        line = line.strip()
        if line:
            lines.append(line)
    
    numbers = ""

    for line in lines:
        for char in line:
            if char.isdigit() or char ==",":
                numbers += char

    sizestr = ""
    fnumber = False
    for char in numbers:
        #this ensures that if there exists a comma before the size, the for loop will still find the correct size
        if char.isdigit()==True:
            fnumber = True
        if char != "," and fnumber == True:
            sizestr += char
        else:
            if fnumber==True:
                break

    size = int(sizestr)

    numbersList = numbers.split(",")
    for item in numbersList:
        try:
            item = int(item)
        except:
            pass

    #getting rid of initial coma and of the size
    del numbersList[0]
    del numbersList[0]

    #create the matrix
    matrix = np.zeros([size,size])#(maybe it needs to be size-1) not sure


    #populate the matrix 
    #know when to stop populating the matrix
    counter = size
    #where the numbers should start from
    start = 1
    city = 0
    generalcounter = 0
    while counter>0:
        for x in range (start,size):
            matrix[city,x] = numbersList[generalcounter]
            generalcounter += 1
        counter -= 1
        city += 1
        start += 1
    #now the matrix is in an upper triangular form
    for i in range(size):
        for j in range(i,size):
            matrix[j][i] = matrix[i][j]
        
    #now the matrix is completely filled in the format of a numpy ndarray
    return (matrix)        