from multiprocessing import parent_process
import random 
import math

def generateChromosome(chromosome_length): #Generate Chromosome
    chromosome = [] #Initialize Chromosome
    for i in range(chromosome_length): #For Chromosome Length
        chromosome.append(random.randint(0,9)) #Append Random Number
    return chromosome
#print(generateChromosome(8))

def generatePopulation(population_size): #Generate Population
    population = [] #Initialize Population
    for i in range(population_size): #For Population Size
        population.append(generateChromosome(8)) #Append Chromosome
    return population   
#print(generatePopulation(100))

def decodeX(chromosome): 
    x_min, x_max = (-5, 5)  #x_min, x_max
    return x_min + ((x_max - x_min)/(9 * 10**(-1) + 9 * 10**(-2)+ 9 * 10**(-3))) * (chromosome[0] * 10 ** (-1) + chromosome[1] * 10 ** (-2) + chromosome[2] * 10 ** (-3))
#print("Decoded X: ", decodeX(generateChromosome(8)))

def decodeY(chromosome):
    y_min, y_max = (-5, 5)  #x_min, x_max
    return y_min + ((y_max - y_min)/(9 * 10**(-1) + 9 * 10**(-2)+ 9 * 10**(-3))) * (chromosome[3] * 10 ** (-1) + chromosome[4] * 10 ** (-2) + chromosome[5] * 10 ** (-3))
#print("Decoded Y: ", decodeX(generateChromosome(8)))

def fitnessFunction(chromosome): #Fitness Function
    x = decodeX(chromosome) #Decode X
    y = decodeY(chromosome) #Decode Y
    return ((math.cos(x)+math.sin(y))**2) / (x**2 + y**2) #Fitness Function
#print("Fitness Function: ", fitnessFunction(generateChromosome(8)))

def evaluate(population, population_size): #menambahkan nilai fitness ke dalam array
    fitness = [] #Initialize Fitness
    for i in range(population_size): #For Population Size
        fitness.append(fitnessFunction(population[i])) #Append Fitness
    return fitness #Return Fitness
#print(evaluate(generatePopulation(100), 100))

def Tournament(population, population_size,tour_size):  #Untuk menseleksi parent
    parent = [] #Initialize Parent
    for i in range (tour_size): #For Tour Size
        indv = population[random.randint(0, population_size-1)] #Append Random Number
        if(parent == [] or fitnessFunction(indv) > fitnessFunction(parent)):    
            parent = indv   #Append Parent
    return parent   #Return Parent
#print(Tournament(generatePopulation(100), 100, 4)) #Menselesi Parent
           
def singlePointCrossover(parent1, parent2, crossoverProbability):   #crossover digunakan untuk mengambil bagian dari individu
    r = random.uniform(0,1) #Random Number
    child1 = [] #Initialize Child 1
    child2 = [] #Initialize Child 2
    if r < crossoverProbability:  #cossover digunakan untuk mengubah individu 
        point = random.randint(1, 4)  #Random Point      
        child1 = parent1[:point] + parent2[point:]  #Child 1
        child2 = parent2[:point] + parent1[point:]  #Child 2
    else:
        child1 = parent1    #Child 1
        child2 = parent2    #Child 2    
    return [child1, child2]
#print(singlePointCrossover(generateChromosome(8), generateChromosome(8), 0.7))

def mutation(child,mutationProbability, chromosome_length): #mutasi digunakan untuk mengubah individu
    v = random.uniform(0,1)
    if v < mutationProbability:
        child[0][random.randint(0,chromosome_length-1)] = random.randint(0,9)
        child[1][random.randint(0,chromosome_length-1)] = random.randint(0,9)
    return child
#print(mutation(singlePointCrossover(generateChromosome(8), generateChromosome(8), 0.7), 0.5, 8))

def elitisme(fitness): #elitisme digunakan untuk memilih individu yang paling baik dan kedua individu yang paling baik
    elit1, elit2 = (0,0)
    for i in range(len(fitness)):
        if fitness[i] < fitness[elit1]:
            elit2 = elit1
            elit1 = i
    return [elit1, elit2]


def generationalReplacement(): #generational Replacement untuk mengganti populasi yang lama untuk yang baru
    population_size = 100
    crossoverProbability = 0.8 #Crossover Probability
    mutationProbability = 0.05 #Mutation Probability
    generation = 75 #Generation
    population = generatePopulation(population_size)
    for i in range(generation):
        newPopulation = []
        fitness = evaluate(population, population_size) #Evaluate
        elit1, elite2 = elitisme(fitness) #Elitisme                                  
        newPopulation.append(population[elit1]) #Append Elit 1
        newPopulation.append(population[elite2])    #Append Elit 2 
        for i in range(population_size//2):     #For Population Size
            parentSelectionA = Tournament(population, population_size, 4)   #Tournament Selection
            parentSelectionB = Tournament(population, population_size, 4)   #Tournament Selection
            while parentSelectionA == parentSelectionB: #While Parent Selection A = Parent Selection B
                parentSelectionB = Tournament(population, population_size, 4)  #Tournament
            child = singlePointCrossover(parentSelectionA, parentSelectionB, crossoverProbability)  #Single Point Crossover
            child = mutation(child, mutationProbability, 8)
            newPopulation.append(child[0])  #Append Child 1
            newPopulation.append(child[1])  #Append Child 2
    population = newPopulation  #Replace Population
    return population

#print(generationalReplacement())

def PrintAll(population, population_size):
    fitness = evaluate(population, population_size) #Evaluate
    elite1, elite2 = elitisme(fitness)  #Elitisme
    BestChromosome = population[elite1] #Best Chromosome
    Bestfitness = fitness[elite1] #Best Fitness
    generation = 75 #Generation
    x = decodeX(BestChromosome) #Decode X
    y = decodeY(BestChromosome) #Decode Y
    print("==========================Result==========================")
    print("Kromosom Terbaik : ", BestChromosome)
    print("X : ", x)
    print("Y : ", y)
    print("=================Tambahan Info============================")
    print("Fitness Terbaik : ", Bestfitness)
    print("Jumlah Generasi : ", generation)
    print("=======================Selesai============================")
    print("\n")

#gen = generationalReplacement()
#PrintAll(gen, 100)