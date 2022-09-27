import random
import numpy
from conf import settings
from views.general_shift_view import GenerateShiftView
from utils.normalize import Normalize
import numpy as np
from utils.hipervolumen import Hipervolumen


def execute_ga(new_population, view, algorithm, num_weights, sol_per_pop, num_generations, num_parents_mating):
    # Defining the population size.
    # The population will have sol_per_pop chromosome where each chromosome has num_weights genes.
    pop_size = (sol_per_pop, num_weights)
    data = []
    for generation in range(num_generations-1):
        # Measuring the fitness of each chromosome in the population.
        fitness = cal_pop_fitness(new_population, view, algorithm)
        data.append([new_population,fitness])

        # Selecting the best parents in the population for mating.
        parents = select_mating_pool(new_population, fitness,num_parents_mating)

        # Generating next generation using crossover.
        offspring_crossover = crossover(parents,offspring_size=(pop_size[0]-parents.shape[0], num_weights))

        # Adding some variations to the offspring using mutation.
        offspring_mutation = mutation(offspring_crossover, algorithm ,  num_mutations= num_weights)

        # Creating the new population based on the parents and offspring.
        new_population[0:parents.shape[0], :] = parents
        new_population[parents.shape[0]:, :] = offspring_mutation
    # Getting the best solution after iterating finishing all generations.
    # At first, the fitness is calculated for each solution in the final generation.
    fitness = cal_pop_fitness(new_population, view, algorithm)
    data.append([new_population,fitness])
    return data


def cal_pop_fitness(population, view: GenerateShiftView, algorithm: str):
    # Calculating the fitness value of each solution in the current population.
    return numpy.array(calculate_fitness_problem(population, view, algorithm))


def select_mating_pool(pop, fitness, num_parents):
    # Selecting the best individuals in the current generation as parents for producing the offspring of the next generation.
    parents = numpy.empty((num_parents, pop.shape[1]))
    for parent_num in range(num_parents):
        min_fitness_idx = numpy.where(fitness == numpy.min(fitness))
        min_fitness_idx = min_fitness_idx[0][0]
        parents[parent_num, :] = pop[min_fitness_idx, :]
        fitness[min_fitness_idx] = 99999999999
    return parents


def crossover(parents, offspring_size):
    offspring = numpy.empty(offspring_size)
    # The point at which crossover takes place between two parents. Usually, it is at the center.
    crossover_point = numpy.uint8(offspring_size[1]/2)
    for k in range(offspring_size[0]):
        # Index of the first parent to mate.
        parent1_idx = k % parents.shape[0]
        # Index of the second parent to mate.
        parent2_idx = (k+1) % parents.shape[0]
        # The new offspring will have its first half of its genes taken from the first parent.
        offspring[k, 0:crossover_point] = parents[parent1_idx, 0:crossover_point]
        # The new offspring will have its second half of its genes taken from the second parent.
        offspring[k, crossover_point:] = parents[parent2_idx, crossover_point:]
    return offspring

def mutation(offspring_crossover, algorithm, num_mutations=1 ):
    mutations_counter = numpy.uint8(offspring_crossover.shape[1] / num_mutations)
    # Mutation changes a number of genes as defined by the num_mutations argument. The changes are random.
    for idx in range(offspring_crossover.shape[0]):
        gene_idx = mutations_counter - 1
        for mutation_num in range(num_mutations):
            # The random value to be added to the gene.
            random_value = get_mutation_value(algorithm , mutation_num)
            offspring_crossover[idx, gene_idx] = offspring_crossover[idx,gene_idx] + random_value
            gene_idx = gene_idx + mutations_counter
    return offspring_crossover

def calculate_fitness_problem(population, view: GenerateShiftView, algorithm: str):
    fitnesss = []
    max_iterations = 30
    for solution in population:
        if algorithm == "GRASP":
            hv_average = 0
            view.algoritmGrasp.setParameters(solution[0], solution[1], solution[2], solution[3])
            for i in range(max_iterations):
                random.seed(settings.SEEDS[i])
                solutions = view.executeGraspToOptimize()
                solutionsNormalized = Normalize().normalizeFitness(solutions)
                pf = np.array(solutionsNormalized)
                hv_average+= Hipervolumen.calculate_hipervolumen_for_optimization(pf)
            fitnesss.append(hv_average/max_iterations)
        else:
            hv_average = 0
            view.algoritmNSGAII.setParameters(solution[0], solution[1], solution[2], solution[3])
            for i in range(max_iterations):
                random.seed(settings.SEEDS[i])
                solutions = view.executeNsgaIIToOptimize()
                solutionsNormalized = Normalize().normalizeFitness(solutions)
                pf = np.array(solutionsNormalized)
                hv_average+= Hipervolumen.calculate_hipervolumen_for_optimization(pf)
            fitnesss.append(hv_average/max_iterations)
    return fitnesss

def get_mutation_value(algorithm, mutation_num):
    if algorithm == "GRASP":
        if mutation_num == 0:
            return numpy.random.randint(0, 10)
        if mutation_num == 1:
            return numpy.random.randint(0, 5)
        if mutation_num == 2:
            return numpy.random.randint(0, 10)
        if mutation_num == 3:
            return numpy.random.randint(0, 2)
    else:    
        if mutation_num == 0:
            return numpy.random.randint(0, 2)
        if mutation_num == 1:
            return numpy.random.randint(0, 2)
        if mutation_num == 2:
            return numpy.random.randint(0, 5)
        if mutation_num == 3:
            return numpy.random.randint(0, 2)