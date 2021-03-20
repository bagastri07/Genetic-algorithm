import random
import copy

def generateChromosome(chrome_size):
    # empty array of choromosome
    chrome = []
    for _ in range(chrome_size):
        chrome.append(random.randint(0, 9))
    return chrome

def generatePopulation(pop_size):
    # empty array of pop
    pop = []
    for _ in range(pop_size):
        pop.append(generateChromosome(8))
    return pop