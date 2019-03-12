
import random 

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

	return totalDistance

# returns the average total distance of the population
def calculateAverageFitness(population, distances):
	avg = 0.0	

	# run evaluate on every member and add the totals, then divide by # members
	for i, member in enumerate(population):
		x = evaluate(member, distances)
		#print "Fitness of", i, "=", x
		avg += x

	avg /= len(population)
	return avg

# returns a sub-population of only those members whose total distances 
# are below the population average
def select(population, distances, size):
	fitnesses = []
	newPopulation = []

	# populate with fitness heuristics
	for i, fitness in enumerate(population):
		fitnesses.append(evaluate(fitness, distances))

	# sort population members based on associated fitness
	population = [x for _,x in sorted(zip(fitnesses, population))]

	# return the "size" members with the lowest associated path length
	for i in range(0, size):
		newPopulation.append(population[i])

	return newPopulation

# just a readable format for testing
def printPopulation(population):
	print "Population:"
	for i, member in enumerate (population):
		print i, "-", member

# create a child for each member (with the next indexed member, 
# less the final member) and add it to the population
def crossover(population, distances):
	newPopulation = population

	# loop over members of population and create new members using each adjacent pair
	for i in range(0, len(population) - 1):
		x = combine(population[i], population[i + 1], distances)
		newPopulation.append(x)
		x = combine(population[i + 1], population[i], distances)
		newPopulation.append(x)

	return newPopulation

# returns the child of two members
def combine(parentOne, parentTwo, distances):
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
def mutate(population):
	
	newPopulation = population
	mod = random.randint(1, 10)

	# loop over population and once every "mod" entries, swap the order of two random values
	for i in range(0, len(newPopulation)):
		if i % mod == 0:
			a = random.randint(0, len(newPopulation[0])-1)
			b = random.randint(0, len(newPopulation[0])-1)
			tmp = newPopulation[i][a]
			newPopulation[i][a] = newPopulation[i][b]
			newPopulation[i][b] = tmp

	return newPopulation


# returns the length of the shortest path and the index it appears in the population
def getLowest(population, distances):
	lowest = evaluate(population[0], distances)
	lowestI = 0

	for i, member in enumerate(population):
		x = evaluate(member, distances)

		if x < lowest:
			lowest = x
			lowestI = i

	return lowest, lowestI


# main algorithms uses everything else to initialize the population, alter it genertically 
# over a defined number of iterations and then returns the shortest path it can find
def travellingSalesmanGenetic(numEntries, sizeEntries, distances, numGenerations):
	population = initialize(numEntries, sizeEntries)

	# loop numGenerations times, select, crossover and mutate the population every iteration
	for i in range (0, numGenerations):
		population =	mutate(
						crossover(
						select(population, distances, numEntries), distances))

	# finally, take the shortest path in the remaining population 
	lowest, lowestIndex = getLowest(population, distances)
	return population[lowestIndex], evaluate(population[lowestIndex], distances)


#############################################################################################
################                            MAIN                             ################
#############################################################################################

numEntries = 100
sizeEntries = 8
numGenerations = 2000

cityList = [	"Brighton", "Bristol", "Cambridge", "Glasgow",
			 	"Liverpool", "London", "Manchester", "Oxford"]

distancesBetweenCities = [
				[0, 	172, 	145, 	607, 	329, 	72, 	312, 	120],
				[172, 	0, 		192, 	494, 	209, 	158, 	216, 	92], 
				[145, 	192,	0,		490,	237, 	75,		205,	100], 
				[607, 	494,	490,	0,		286,	545,	296, 	489], 
				[329,	209,	237,	286,	0,		421,	49,		208], 
				[72,	158,	75,		545,	421,	0,		249,	75], 
				[312,	216,	205,	296,	49,		249,	0,		194], 
				[120,	92,		100,	489,	208,	75,		194,	0]]

bestPath, distance = travellingSalesmanGenetic(numEntries, sizeEntries, distancesBetweenCities, numGenerations)

print "Shortest path:", cityList[bestPath[0]],
for i, city in enumerate(bestPath[1:]):
	print  "->", cityList[city],
print "\nTotal Distance: ", distance