import random
import copy
import math

def generate_chromosome(chrom_size):
    # empty array of choromosome
    chrom = []
    for _ in range(chrom_size):
        chrom.append(random.randint(0, 1))
    return chrom

def generate_population(pop_size):
    # empty array of pop
    pop = []
    for _ in range(pop_size):
        pop.append(generate_chromosome(8))
    return pop

def decode_chromosome(chrom):
    x_max, x_min = (2, -1)
    y_max, y_min = (1, -1)

    x = x_min + (x_max - x_min / (2**-1 + 2**-2 + 2**-3 + 2**-4)) * (chrom[0] * 2**-1 + chrom[1] * 2**-2 + chrom[2] * 2**-3 + chrom[3] * 2**-4)
    y = y_min + (y_max - y_min / (2**-1 + 2**-2 + 2**-3 + 2**-4)) * (chrom[4] * 2**-1 + chrom[5] * 2**-2 + chrom[6] * 2**-3 + chrom[7] * 2**-4)

    return [x, y]

def objective_function(x, y):
    
    return ((math.cos(x**2)) * (math.sin(y**2))) + (x + y)

def count_fitness(chrom):
    decoded_value = decode_chromosome(chrom)
    return objective_function(decoded_value[0], decoded_value[1])

def evaluate(pop, pop_size):
    all_fit = []
    
    for i in range(pop_size):
        all_fit.append(count_fitness(pop[i]))
    
    return all_fit

def tournament_selection(pop, pop_size, tour_size):
    best_chrom = []
    for _ in range(1, tour_size):
        chrom = pop[random.randint(0, pop_size-1)]
        if (best_chrom == [] or (count_fitness(best_chrom) < count_fitness(chrom))):
            best_chrom = chrom
    return best_chrom

def recombination(parrent_a, parrent_b, recom_prob):
    random_value = random.uniform(0, 1) 
    if (random_value < recom_prob):
        point = random.randint(1, 7)
        for i in range (point):
            parrent_a[i], parrent_b[i] = parrent_b[i], parrent_a[i]

    return [parrent_a, parrent_b]

def mutation(offspring, mut_prob):
    random_value = random.uniform(0, 1)
    if (random_value < mut_prob):
        offspring[0][random.randint(0, 7)] = random.randint(0, 1)
        offspring[1][random.randint(0, 7)] = random.randint(0, 1)

    return offspring

def elitisme(all_fit):
    copy_all_fit = copy.deepcopy(all_fit)
    copy_all_fit.sort()

    best_index = all_fit.index(max(all_fit))
    second_index = all_fit.index(copy_all_fit[-2])
        
    return [best_index, second_index]

def main():
    # hyper paramaters
    pop_size, tour_size, generation, recom_prob, mut_prob = (40, 7, 100, 0.6, 0.05)

    iteration = 0
    population = generate_population(pop_size)
    fitness = evaluate(population, pop_size)

    while(iteration < generation and max(fitness) < 2.3):
        fitness = evaluate(population, pop_size)
        
        new_population = []

        best_index = elitisme(fitness)
        new_population.extend([population[best_index[0]], population[best_index[1]]])

        for  _ in range(0, pop_size-2, 2):
            parrent_a = tournament_selection(population, pop_size, tour_size)
            parrent_b = tournament_selection(population, pop_size, tour_size)

            while(parrent_b == parrent_a):
                parrent_b = tournament_selection(population, pop_size, tour_size)
            copy_parrent_a = copy.deepcopy(parrent_a)
            copy_parrent_b = copy.deepcopy(parrent_b)
            offsprings = recombination(copy_parrent_a, copy_parrent_b, recom_prob)
            offsprings = mutation(offsprings, mut_prob)
            new_population.extend(offsprings)
        population = new_population
        iteration+=1
    
    fitness = evaluate(population, pop_size)
    result_index = elitisme(fitness)

    print('The Result of Maximizing the Function:')
    print()
    print('Best Chromosome         :', population[result_index[0]])
    print('Best fitness            :', count_fitness(population[result_index[0]]))
    print('Decoded Value           :', decode_chromosome(population[result_index[0]]))
    print('Total Generation        :', iteration)

    # Test 1
    # Best Chromosome         : [1, 0, 1, 0, 1, 1, 1, 1]
    # Best fitness            : 2.2798718011868155
    # Decoded Value           : [0.9166666666666665, 0.9374999999999998]
    # Total Generation        : 2

    # Test 2
    # Best Chromosome         : [1, 0, 1, 0, 1, 1, 1, 1]
    # Best fitness            : 2.2798718011868155
    # Decoded Value           : [0.9166666666666665, 0.9374999999999998]
    # Total Generation        : 4

    # Test 3
    # Best Chromosome         : [1, 0, 1, 1, 1, 1, 1, 1]
    # Best fitness            : 2.260035057580861
    # Decoded Value           : [1.1083333333333334, 0.9374999999999998]
    # Total Generation        : 55
    
main()

