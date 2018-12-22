import time
import math
import random as r
import numpy as np
import readfile
import sys

#this function focuses on making the arrays correspond to tours after the crossover
def findduplicates(tour):
    missing = []
    seen = []
    for i in range(1,len(tour)+1):
        if (i in tour)==False:
            missing.append(i) #if a city is missing (cities are sequential in the examples) it is added to the array
    counter = len(missing)
    for city in range(0,len(tour)):
        if counter==0:
            break
        if tour[city] in seen: # if a city has been seen before then its a duplicate so it is replaced with a missing one
            tour[city] = missing[counter-1] 
            counter -= 1
        else:
            seen.append(tour[city])
    return tour

#sum the distances between the cities to find the length of the tours.
def fitness(population,distances):
    size = len(population[1][1:])
    for i in range (len(population)):
        fit = 0
        #calulating the distance and adding it to the fitness
        for j in range (2,(size+1)):
            c1 = int(population[i][j])-1
            c2 = int(population[i][j-1])-1
            fit += distances[c1][c2]
        #adding the distance from the final city to the first one 
        c1 = int(population[i][1])-1
        c2 = int(population[i][size])-1
        fit += distances[c1][c2]
        population[i][0] = fit
    #return the given population with the distance added
    return population

#this function calculates each individual probability of an individual being selected as a parent. more details can be found in the report
def calculateprob(population):
    prob = np.ndarray((len(population)))
    sigma_fitness = 0
    #add all the fitnesses
    for i in range ((len(population))):
        sigma_fitness += population[i][0]

    for i in range(len(population)):
        prob[i] = population[i][0]/sigma_fitness
    return (prob)

#this function finds the fittes individual for a given population, basic minimum search
def find_fittest(population):
    fittest = population[0][0]
    position = 0
    for i in range(len(population)):
        if population[i][0] < fittest:
            fittest = population[i][0]
            position = i
    return (fittest,position)

def genetic(filename):
    distances = readfile.read(filename)
    size = len(distances)

    mutateprob = 0.4 #probability that the child is mutated
    generations = 400 #number of populations created 
    population_size = 250 #size of tours that each population has
    population = np.zeros((population_size,size+1),np.int64)
    # If elitism is true, it means that the fittest tour of each population will be moved to the new Population in order to improve performance of the genetic algorithm. The tour will be swapped with a random chosen tour but we can also find the most unfit individual and swap that over with the fittest for better results. However, in that case you are interfiring with the random selection and probability.
    elitism = True

    #initiate the population
    cities = np.zeros((size),np.int64)
    for i in range(size):
        cities[i] = (i+1)

    # randomly shuffle all the cities of the initial population
    for i in range(population_size):
        r.shuffle(cities)            

        for j in range(size):
            population[i][j+1] = cities[j]


    start = time.time()
    while True:
        #initiate the new population, calculate the fitness and probability of the old one
        newP = np.zeros((population_size,size+1),np.int)
        population = fitness(population,distances)
        probs = calculateprob(population)
        for i in range (len(population)):
            # initiate the parents
            newX = np.zeros((size+1),np.int)
            newY = np.zeros((size+1),np.int)
            
            #choose the parents based on the probabilities
            x = np.random.choice(len(population),p=probs)
            y = np.random.choice(len(population),p=probs)
            #choose a random position to split the tours
            crossover = r.randint(1,size-1)
            #add the prefixes to the parents
            newX[1:crossover+1] = population[x][1:crossover+1]
            newY[1:crossover+1] = population[y][1:crossover+1]
            #add the suffixes to the opposite parents
            newX[crossover+1:size+1] =  population[y][crossover+1:size+1]
            newY[crossover+1:size+1] =  population[x][crossover+1:size+1]
            #replace duplicate cities with missing cities so that a tour exist
            newX[1:] = findduplicates(newX[1:])
            newY[1:] = findduplicates(newY[1:])
            #find fitness of children and choose the fittest one (the one with the smallest length)
            children = fitness((newX,newY),distances)

            if children[0][0]<children[1][0]:
                z = children[0]
            else:
                z = children[1]
            #mutate the child z with fixed probability
            if r.random() < mutateprob:
                city1 = np.random.choice(1,len(z))
                city2 = np.random.choice(1,len(z))
                temp = z[city1]
                z[city1] = z[city2]
                z[city2] = temp
            
            newP[i][:] = z
        #if elitism is set to true then it picks a random position to place the elite in the new population
        if elitism == True:
            position = r.randint(0,len(population)-1)
            elit = find_fittest(population)
            newP[position][:] = population[elit[1]][:]

        population = newP
        if generations==0:
            break
        else: 
            generations -= 1

    end = time.time()


    print ("Total Time Taken: ",end-start)
    best_tour = find_fittest(population)
    print ("Best tour that was found has length: ", best_tour[0])
    pointer = best_tour[1]
    print ("The actual tour is: ", population[pointer][1:])
    final = population[pointer]
    return final

#just change the filename for it to work
tour = genetic("AISearchfile017.txt")
readfile.write("AISearchfile017.txt",len(tour[1:]),tour[0],tour[1:])
