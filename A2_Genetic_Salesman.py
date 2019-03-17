
import random 
import matplotlib.pyplot as plt
import numpy as np
import math

# returns random list of integers, non repeating, within the range
# to represent members of the population
def initialize(numEntries, sizeEntries):
	population = []

	# loop numEntries times and add unique random integers to each index
	for i in range (0, numEntries):

		# while True + break is like do while loop
		while True:
		    member = random.sample(range(0, sizeEntries), sizeEntries)

		    if member not in population:
		    	population.append(member)
		    	break

	return population

# returns the total distance of a member 
def evaluate(member, distances):
	totalDistance = 0;

	# add the distances between each city on the path
	for i in range(0, len(member) - 1):

		x = distances[member[i]][member[i + 1]]
		totalDistance += x

	# distance from last stop back to start
	totalDistance += distances[member[-1:][0]][ member[0]]
	return 1.0/totalDistance

# returns a sub-population of only those members whose total distances 
# are below the population average
def truncationSelect(population, distances, size):
	fitnesses = []
	newPopulation = []

	# populate with fitness heuristics
	for i, fitness in enumerate(population):
		fitnesses.append(evaluate(fitness, distances))

	# sort population members based on associated fitness
	population = [x for _,x in sorted(zip(fitnesses, population), reverse=True)]

	for i in range(0, size):
		newPopulation.append(population[i])

	return newPopulation

# ranomly selects members for the next generation but probability of 
# being selected is weighted by fitness
def rouletteSelect(population, distances, size):
	total=0.0
	probabilities = [0]
	newPopulation = []
	fitnesses = []

	# selects fittest result automatically
	a, b = getFittest(population, distances)
	newPopulation.append(population[b])

	# run evaluate on every member and add the totals
	for i, member in enumerate(population):
		x = evaluate(member, distances)
		total += x

	# get the probabilities 
	for i, member in enumerate(population):
		if i!=0 :
			probabilities.append(probabilities[i-1] + evaluate(member, distances)/total)

	# loop until newPopulation is filled 
	while len(newPopulation) < size:
		x = random.uniform(0, 1.0)
		for i, member in enumerate(population):
			if (i >= len(population)-1):
				if (member not in newPopulation):
					newPopulation.append(member)
				break

			if (x >= probabilities[i] and x < probabilities[i+1]):
				if (member not in newPopulation):
					newPopulation.append(member)
				break

	return newPopulation



# just a readable format for testing
def printPopulation(population, distances):
	print "Population:"
	for i, member in enumerate (population):
		print i, "-", member, evaluate(member, distances), 1.0/evaluate(member, distances)

# create a child for each member (with the next indexed member, 
# less the final member) and add it to the population
def twinCrossover(population, distances, sizeEntries):
	newPopulation = population
	size = len(population) * 3
	# loop over members of population and create new members using each adjacent pair
	for i in range(0, len(population) - 1):
		
		x = twinCombine(population[i], population[i + 1], distances)
		if x not in newPopulation:
			newPopulation.append(x)
		x = twinCombine(population[i + 1], population[i], distances)
		if x not in newPopulation:
			newPopulation.append(x)

	while (len(newPopulation) < size):
		member = random.sample(range(0, sizeEntries), sizeEntries)
		if member not in newPopulation:
			newPopulation.append(member)

	return newPopulation


def ocCrossover(population, distances, sizeEntries):
	newPopulation = population
	size = len(population) * 2
	for i in range(0, len(population) - 1):
		a, b = findShortestdistance(population[i], distances)
		c, d = findShortestdistance(population[i+1], distances)

		member = []
		for j in range(0, len(population[i])):
			if (j == a or j == b):
				if population[i][j] not in member:
					member.append(population[i][j])
			if(j == c or j == d):
				if population[i+1][j] not in member:
					member.append(population[i+1][j])
			if (len(member) <= j):
				while True:
					x = random.randint(0, len(population[i])-1)

					if x not in member:
						member.append(x)
						break


		if member not in newPopulation:
			newPopulation.append(member)
	while (len(newPopulation) < size):
		member = random.sample(range(0, sizeEntries), sizeEntries)
		if member not in newPopulation:
			newPopulation.append(member)
	return newPopulation



# returns the child of two members
def twinCombine(parentOne, parentTwo, distances):
	child = []
	a, b = findShortestdistance(parentOne, distances)
	j = 0

	# take two closest adjacent cities in the first parent, take them for the child
	# and populate the rest of the child with the other parent
	for i in range(0, len(parentOne)):
		if(i!=a and i!=b):
			while(parentTwo[j]==parentOne[a] or parentTwo[j]==parentOne[b]):
				j+=1

			child.append(parentTwo[j])
			j+=1

		else:
			child.append(parentOne[i])

	return child



# return indices where a member's distance between two adjacent 
# indices is shortest
def findShortestdistance(member, distances):
	a = 0
	b = 1
	shortest = distances[member[0]][member[1]]

	# loop over cities in member and find the shortest distance
	for i in range(0, len(member) - 1):
		x = distances[member[i]][member[i + 1]]

		if x < shortest:
			shortest = x
			a = i
			b = i + 1

	return a, b

# returns the population after selecting members at random and switching two values in each
# introduces randomness to genetic algorithm
def mutate(population, mod):
	#print population[0]
	newPopulation = population
	#print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1"
	if mod == 0:
		mod = random.randint(1, 5)

	x = []
	for j in range(0, len(newPopulation[0])):
		x.append(newPopulation[0][j])
	y = False
	
	# loop over population and once every "mod" entries, swap the order of two random values
	for i in range(5, len(newPopulation)):
		for j in range(0, len(x)):
			if x[j] != newPopulation[0][j]:
				y = True
		if (y):
			#print "---->"
			y = False
		#print newPopulation[0], i
		if i % mod == 0:
			a = random.randint(0, len(newPopulation[i])-1)
			b = random.randint(0, len(newPopulation[i])-1)
			#print i, a, b
			tmp = newPopulation[i][a]
			newPopulation[i][a] = newPopulation[i][b]
			newPopulation[i][b] = tmp
	#print "!!!!!!!!!!!!!!!!!!!!!!!!!!!"
	return newPopulation


# returns the length of the shortest path and the index it appears in the population
def getFittest(population, distances):
	lowest = 1.0/evaluate(population[0], distances)
	lowestI = 0

	for i, member in enumerate(population):
		x = 1.0/ evaluate(member, distances)

		if x < lowest:
			lowest = x
			lowestI = i

	return lowest, lowestI

def getDistances(locations):
	distances = []

	for i in range(0, len(locations)):
		distancesI = []
		for j in range(0, len(locations)):

			dist = math.hypot(locations[i][0] - locations[j][0], locations[i][1] - locations[j][1])
			distancesI.append(dist)
		distances.append(distancesI)
	return distances

def plotCities(locations):
	plt.xticks(np.arange(0, 201, 20))
	plt.yticks(np.arange(0, 201, 20))
	plt.grid(True)

	x = []
	y = []

	for i in range(0, len(locations)):
		#plt.plot(cityLocations)
		#plt.plot(cityLocations[i][0], cityLocations[i][1], "ro-")
		x.append(locations[i][0])
		y.append(locations[i][1])

	for i in range(0, len(locations), 1):
	    plt.plot(x[i:i+2], y[i:i+2], 'ro-')

	plt.show()

def sortByPath(path, locations):
	sortedLocations = []
	for i in path:
		sortedLocations.append(locations[i])
	return sortedLocations


def testHarness2(numTests):

	selection = input("Which Problem Domain would you like to use?\n1.\tFirst Domain (Graphical Representation)\n2.\tSecond Domain (No Grphical Representation, Britain Example)\n3.\tRun tests on second Problem Domain\n")
	if selection == 1:
		cityLocations = 	[	[20, 20],
								[20, 40],
								[20, 160],
								[40, 120],
								[60, 20],
								[60, 80],
								[60, 200],
								[80, 180],
								[100, 40],
								[100, 120],
								[100, 160],
								[120, 80],
								[140, 140],
								[140, 180],
								[160, 20],
								[180, 60],
								[180, 100],
								[180, 200],
								[200, 40],
								[200, 160]]

		distances = getDistances(cityLocations)

		# numEntries must be < sizeEntries! factorial
		numEntries = 500
		sizeEntries = len(cityLocations) -1
		#print sizeEntries
		numGenerations = 1000
		#print distances[0]
		bestPath, distance, gensTaken = TSG_Truncation_Twin(numEntries, sizeEntries, distances, numGenerations, 0, 0)

		cityLocations = sortByPath(bestPath, cityLocations)

		print "Shortest path:", bestPath[0],
		for i, city in enumerate(bestPath[1:]):
			print  "->", bestPath[i],
		print "\nTotal Distance: ", distance


		plotCities(cityLocations)



	if (selection == 2 or selection == 3):
		numEntries = 50
		sizeEntries = 8
		numGenerations = 2000

		cityList = [	"Brighton", "Bristol", "Cambridge", "Glasgow",
					 	"Liverpool", "London", "Manchester", "Oxford"]

		distances = [
						[0, 	172, 	145, 	607, 	329, 	72, 	312, 	120],
						[172, 	0, 		192, 	494, 	209, 	158, 	216, 	92], 
						[145, 	192,	0,		490,	237, 	75,		205,	100], 
						[607, 	494,	490,	0,		286,	545,	296, 	489], 
						[329,	209,	237,	286,	0,		421,	49,		208], 
						[72,	158,	75,		545,	421,	0,		249,	75], 
						[312,	216,	205,	296,	49,		249,	0,		194], 
						[120,	92,		100,	489,	208,	75,		194,	0]]


	if selection == 2:

		bestPath, distance, gensTaken = TSG_Truncation_Twin(numEntries, sizeEntries, distances, numGenerations, 0, 0)

		print "Shortest path:", cityList[bestPath[0]],
		for i, city in enumerate(bestPath[1:]):
			print  "->", cityList[city],
		print "\nTotal Distance: ", distance



	if selection == 3:
		selection = input("Which version of the algorithm would you like to use?\n1.\tTruncation Selection & Only Child Crossover\n2.\tTruncation Selection & Twin Crossover\n3.\tRoulette Selection and Only Child Crossover\n4.\tRoulette Selection and Twin Crossover\n")
		mod = input("What would you like to use for the upper bound for mutation? (higher -> less likely for members to mutate)")



		if selection == 1:

			bestPath, distance, gensTaken = TSG_Truncation_OC(numEntries, sizeEntries, distances, numGenerations, 0, mod)
			print distance
			terminationCondition = distance
			avg = 0

			for i in range (0, numTests):
				bestPath, distance, gensTaken = TSG_Truncation_OC(numEntries, sizeEntries, distances, numGenerations, terminationCondition, mod)
				#print "Terminated after ", gensTaken, "with distance ", distance
				avg += gensTaken

			avg/=numTests

			print "Using Truncation Selection & Only Child Crossover, Average # Generations to achieve target fitness is", avg


		if selection == 2:

			bestPath, distance, gensTaken = TSG_Truncation_Twin(numEntries, sizeEntries, distances, numGenerations, 0, 0)
			print distance
			terminationCondition = distance
			avg = 0

			for i in range (0, numTests):
				bestPath, distance, gensTaken = TSG_Truncation_Twin(numEntries, sizeEntries, distances, numGenerations, terminationCondition, mod)
				#print "Terminated after ", gensTaken, "with distance ", distance
				avg += gensTaken

			avg/=numTests

			print "Using Truncation Selection & Twin Crossover, Average # Generations to achieve target fitness is", avg


		if selection == 3:

			bestPath, distance, gensTaken = TSG_Roulette_OC(numEntries, sizeEntries, distances, numGenerations, 0, 0)
			print distance
			terminationCondition = distance
			avg = 0

			for i in range (0, numTests):
				bestPath, distance, gensTaken = TSG_Roulette_OC(numEntries, sizeEntries, distances, numGenerations, terminationCondition, mod)
				#print "Terminated after ", gensTaken, "with distance ", distance
				avg += gensTaken

			avg/=numTests

			print "Using Roulette Selection & Only Child Crossover, Average # Generations to achieve target fitness is", avg

		if selection == 4:	
	
			bestPath, distance, gensTaken = TSG_Roulette_Twin(numEntries, sizeEntries, distances, numGenerations, 0, 0)
			print distance
			terminationCondition = distance
			avg = 0

			for i in range (0, numTests):
				bestPath, distance, gensTaken = TSG_Roulette_Twin(numEntries, sizeEntries, distances, numGenerations, terminationCondition, mod)
				#print "Terminated after ", gensTaken, "with distance ", distance
				avg += gensTaken

			avg/=numTests

			print "Using Roulette Selection & Tein Crossover, Average # Generations to achieve target fitness is", avg



############################################################################################
######                            Travelling Salesman Algorithms                     ########
############################################################################################


# main algorithms uses everything else to initialize the population, alter it genertically 
# over a defined number of iterations and then returns the shortest path it can find
def TSG_Truncation_OC(numEntries, sizeEntries, distances, numGenerations, terminationCondition, mod):
	population = initialize(numEntries, sizeEntries)


	# loop numGenerations times, select, crossover and mutate the population every iteration
	for i in range (0, numGenerations):
		gensTaken = i
		population =	mutate(
						ocCrossover(
						truncationSelect(population, distances, numEntries), distances, sizeEntries), mod)

		if (terminationCondition != 0):
			lowest, lowestIndex = getFittest(population, distances)
			if (lowest <= terminationCondition):
				break;

	# finally, take the shortest path in the remaining population 
	lowest, lowestIndex = getFittest(population, distances)
	return population[lowestIndex], 1.0/evaluate(population[lowestIndex], distances), gensTaken

def TSG_Roulette_OC(numEntries, sizeEntries, distances, numGenerations, terminationCondition, mod):
	population = initialize(numEntries, sizeEntries)

	# loop numGenerations times, select, crossover and mutate the population every iteration
	for i in range (0, numGenerations):
		gensTaken = i
		population =	mutate(
						ocCrossover(
						rouletteSelect(population, distances, numEntries), distances, sizeEntries), mod)

		if (terminationCondition != 0):
			lowest, lowestIndex = getFittest(population, distances)
			if (lowest <= terminationCondition):
				break;

	# finally, take the shortest path in the remaining population 
	lowest, lowestIndex = getFittest(population, distances)
	return population[lowestIndex], 1.0/evaluate(population[lowestIndex], distances), gensTaken

def TSG_Truncation_Twin(numEntries, sizeEntries, distances, numGenerations, terminationCondition, mod):
	population = initialize(numEntries, sizeEntries)


	# loop numGenerations times, select, crossover and mutate the population every iteration
	for i in range (0, numGenerations):
		gensTaken = i
		population =	mutate(
						twinCrossover(
						truncationSelect(population, distances, numEntries), distances, sizeEntries), mod)

		if (terminationCondition != 0):
			lowest, lowestIndex = getFittest(population, distances)
			if (lowest <= terminationCondition):
				break;


	# finally, take the shortest path in the remaining population 
	lowest, lowestIndex = getFittest(population, distances)
	return population[lowestIndex], 1.0/evaluate(population[lowestIndex], distances), gensTaken

def TSG_Roulette_Twin(numEntries, sizeEntries, distances, numGenerations, terminationCondition, mod):
	population = initialize(numEntries, sizeEntries)


	# loop numGenerations times, select, crossover and mutate the population every iteration
	for i in range (0, numGenerations):
		gensTaken = i
		population =	mutate(
						twinCrossover(
						rouletteSelect(population, distances, numEntries), distances, sizeEntries), mod)

		if (terminationCondition != 0):
			lowest, lowestIndex = getFittest(population, distances)
			if (lowest <= terminationCondition):
				break;

	# finally, take the shortest path in the remaining population 
	lowest, lowestIndex = getFittest(population, distances)
	return population[lowestIndex], 1.0/evaluate(population[lowestIndex], distances), gensTaken


#############################################################################################
################                            MAIN   1                         ################
#############################################################################################

# numEntries = 50
# sizeEntries = 8
# numGenerations = 2000

# cityList = [	"Brighton", "Bristol", "Cambridge", "Glasgow",
# 			 	"Liverpool", "London", "Manchester", "Oxford"]

# distances = [
# 				[0, 	172, 	145, 	607, 	329, 	72, 	312, 	120],
# 				[172, 	0, 		192, 	494, 	209, 	158, 	216, 	92], 
# 				[145, 	192,	0,		490,	237, 	75,		205,	100], 
# 				[607, 	494,	490,	0,		286,	545,	296, 	489], 
# 				[329,	209,	237,	286,	0,		421,	49,		208], 
# 				[72,	158,	75,		545,	421,	0,		249,	75], 
# 				[312,	216,	205,	296,	49,		249,	0,		194], 
# 				[120,	92,		100,	489,	208,	75,		194,	0]]

# bestPath, distance, gensTaken = travellingSalesmanGenetic(numEntries, sizeEntries, distances, numGenerations, 1355)

# print "Shortest path:", cityList[bestPath[0]],
# for i, city in enumerate(bestPath[1:]):
# 	print  "->", cityList[city],
# print "\nTotal Distance: ", distance


#############################################################################################
################                            MAIN   2                         ################
#############################################################################################



# cityLocations = 	[	[20, 20],
# 						[20, 40],
# 						[20, 160],
# 						[40, 120],
# 						[60, 20],
# 						[60, 80],
# 						[60, 200],
# 						[80, 180],
# 						[100, 40],
# 						[100, 120],
# 						[100, 160],
# 						[120, 80],
# 						[140, 140],
# 						[140, 180],
# 						[160, 20],
# 						[180, 60],
# 						[180, 100],
# 						[180, 200],
# 						[200, 40],
# 						[200, 160]]



# distances = getDistances(cityLocations)

# # numEntries must be < sizeEntries! factorial
# numEntries = 500
# sizeEntries = len(cityLocations) -1
# #print sizeEntries
# numGenerations = 1000
# #print distances[0]
# bestPath, distance = travellingSalesmanGenetic(numEntries, sizeEntries, distances, numGenerations, 0)

# cityLocations = sortByPath(bestPath, cityLocations)


# print "Shortest path:", bestPath[0],
# for i, city in enumerate(bestPath[1:]):
# 	print  "->", bestPath[i],
# print "\nTotal Distance: ", distance


# plotCities(cityLocations)



# #############################################################################################
# ################                            TESTING 1                        ################
# #############################################################################################


# numEntries = 50
# sizeEntries = 8
# numGenerations = 2000

# cityList = [	"Brighton", "Bristol", "Cambridge", "Glasgow",
# 			 	"Liverpool", "London", "Manchester", "Oxford"]

# distances = [
# 				[0, 	172, 	145, 	607, 	329, 	72, 	312, 	120],
# 				[172, 	0, 		192, 	494, 	209, 	158, 	216, 	92], 
# 				[145, 	192,	0,		490,	237, 	75,		205,	100], 
# 				[607, 	494,	490,	0,		286,	545,	296, 	489], 
# 				[329,	209,	237,	286,	0,		421,	49,		208], 
# 				[72,	158,	75,		545,	421,	0,		249,	75], 
# 				[312,	216,	205,	296,	49,		249,	0,		194], 
# 				[120,	92,		100,	489,	208,	75,		194,	0]]


# #print rouletteSelect(initialize(numEntries, sizeEntries), distances, numEntries)


# numTests = 200
# print testHarness(numEntries, sizeEntries, distances, numGenerations, numTests)


testHarness2(200)