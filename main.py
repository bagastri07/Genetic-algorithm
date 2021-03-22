import random
import copy
import math

def generate_chromosome(chrom_size):
    # empty array of choromosome
    chrom = []
    for _ in range(chrom_size):
        chrom.append(random.randint(0, 9))
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

    x = x_min + (x_max - x_min / (9 * (10**-1 + 10**-2 + 10**-3 + 10**-4))) * (chrom[0] * 10**-1 + chrom[1] * 10**-2 + chrom[2] * 10**-3 + chrom[3] * 10**-4)
    y = y_min + (y_max - y_min / (9 * (10**-1 + 10**-2 + 10**-3 + 10**-4))) * (chrom[4] * 10**-1 + chrom[5] * 10**-2 + chrom[6] * 10**-3 + chrom[7] * 10**-4)

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
    for _ in range(tour_size):
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

def mutation(offsprings, mut_prob):
    random_value = random.uniform(0, 1)
    if (random_value < mut_prob):
        offsprings[0][random.randint(0, 7)] = random.randint(0, 9)
        offsprings[1][random.randint(0, 7)] = random.randint(0, 9)

    return offsprings

def elitisme(all_fit):
    copy_all_fit = copy.deepcopy(all_fit)
    copy_all_fit.sort()

    best_index = all_fit.index(copy_all_fit[-1])
    second_index = all_fit.index(copy_all_fit[-2])
        
    return [best_index, second_index]

def elitisme_process(pop, new_pop, fitness):
    indexs = elitisme(fitness)
    new_pop.extend([pop[indexs[0]], pop[indexs[1]]])

def print_result(pop, pop_size, iteration):
    fitness = evaluate(pop, pop_size)
    result_index = elitisme(fitness)
    decoded_value = decode_chromosome(pop[result_index[0]])

    print('The Result of Maximizing the Function:')
    print()
    print('Best Chromosome         :', pop[result_index[0]])
    print('Best fitness            :', count_fitness(pop[result_index[0]]))
    print('Decoded X Value         :', decoded_value[0])
    print('Decoded Y Value         :', decoded_value[1])
    print('Total Generation        :', iteration)

def main():
    # hyper paramaters
    pop_size, tour_size, generation, recom_prob, mut_prob = (50, 5, 200, 0.6, 0.09)

    iteration = 0
    population = generate_population(pop_size)
    fitness = evaluate(population, pop_size)

    while(iteration < generation and max(fitness) < 2.48):
        fitness = evaluate(population, pop_size)
        
        new_population = []

        elitisme_process(population, new_population, fitness)

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

    print_result(population, pop_size, iteration)
    
    # Test 1
    # Best Chromosome         : [6, 2, 3, 8, 9, 9, 9, 5]
    # Best fitness            : 2.480105475185494
    # Decoded X Value         : 0.8714623862386242
    # Decoded Y Value         : 0.9990999599959991
    # Total Generation        : 14

    # Test 2
    # Best Chromosome         : [6, 2, 2, 9, 9, 9, 9, 9]
    # Best fitness            : 2.4815482828907784
    # Decoded X Value         : 0.8687622962296231
    # Decoded Y Value         : 0.9998999999999998
    # Total Generation        : 41

    # Test 3
    # Best Chromosome         : [5, 9, 9, 9, 9, 9, 9, 9]
    # Best fitness            : 2.4747064877314284
    # Decoded X Value         : 0.7997599959995998
    # Decoded Y Value         : 0.9998999999999998
    # Total Generation        : 120
    
main()

