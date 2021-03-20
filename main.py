import random
import copy
import math

def generateChromosome(chrom_size):
    # empty array of choromosome
    chrom = []
    for _ in range(chrom_size):
        chrom.append(random.randint(0, 1))
    return chrom

def generatePopulation(pop_size):
    # empty array of pop
    pop = []
    for _ in range(pop_size):
        pop.append(generateChromosome(8))
    return pop

def  decodeChromosome(chrom):
    xMax = 2
    xMin = -1
    yMax = 1
    yMin = -1

    x = xMin + (xMax - xMin / (2**-1 + 2**-2 + 2**-3 + 2**-4)) * (chrom[0] * 2**-1 + chrom[1] * 2**-2 + chrom[2] * 2**-3 + chrom[3] * 2**-4)
    y = yMin + (yMax - yMin / (2**-1 + 2**-2 + 2**-3 + 2**-4)) * (chrom[4] * 2**-1 + chrom[5] * 2**-2 + chrom[6] * 2**-3 + chrom[7] * 2**-4)

    return [x, y]

def objectiveFunc(x, y):
    return (math.cos(x**2) * math.cos(y**2)) + (x + y)

def countFitness(chrom):
    decoded_value = decodeChromosome(chrom)
    return objectiveFunc(decoded_value[0], decoded_value[1])

# main section
A = generateChromosome(8)
print(A)
print(countFitness(A))