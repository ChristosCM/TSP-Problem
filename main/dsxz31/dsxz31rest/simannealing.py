import time 
import readfile #own script that reads the files
import numpy as np
import random as r
import math
import sys




#this function picks a random i and k and reverses the city between them
def permutate(tour):
    i = r.randint(0,len(tour)-1)
    k = r.randint(i,len(tour)-1)
    newTour = np.zeros((len(tour)),np.int)
    start = tour[0:i]
    middle = tour [i:k]
    end = tour[k:]
    middle = middle[::-1]
    newTour[0:i] = start 
    newTour[i:k] = middle
    newTour[k:] = end
    return newTour


def fitness(state,distances):
    fit = 0
    size = len(distances)
        #calulating the distance and adding it to the fitness
    for j in range (2,(size+1)):
        c1 = int(state[j])-1
        c2 = int(state[j-1])-1
        fit += distances[c1][c2]
    #adding the distance from the final city to the first one 
    c1 = int(state[1])-1
    c2 = int(state[size])-1
    fit += distances[c1][c2]
    state[0] = fit
    #return the given population with the distance added
    return state

def siman(filename):

    distances = readfile.read(filename) # reading the file from the readfile.py
    size = (len(distances))

    e = math.e
    cities = np.zeros((size),np.int)
    #initiate the cities 
    for i in range(0,size):
        cities[i] = i+1
    current = np.zeros((size+1),np.int)
    current[0] = 0
    current[1:] = np.random.permutation(cities)
    #these are variables for the other scheduling algorithms 
    schedule = []
    schedule.append(500) #this is user defined
    a = 0.95
    T = 10000
    best_fit = np.zeros((size+1),np.int)
    best_fit[0] = 9999999
    start = time.time()
    for t in range (1,10000000,4):
        #schedue.append(schedule[t-1]/beta)
        #T = a * T
        T =  1/(math.log(1+t))
        succ = np.zeros((size+1))
        temp = np.zeros((size+1))
        if T <0.1:
            break        
        temp[1:] = current[1:]
        succ[1:] = permutate(temp[1:])
        current = fitness(current,distances)
        succ = fitness(succ,distances)
        difference = succ[0] - current[0]
        if  difference >= 0:
            current = succ
        else:
            
            if r.random() < (e**(((-(difference))/T))):
                current[:] = succ[:]
        if current[0] < best_fit[0]:
            best_fit = current
        
    end = time.time()
    print (end-start)
    # print ("The simulated annealing has produced a tour of lenght: " , current[0])
    # print ("The actual tour is: ", current[1:])
    return current # best_fit

tour = siman("AISearchfile535.txt")
readfile.write("AISearchfile535.txt",len(tour[1:]),tour[0],tour[1:])