from concurrent.futures import ThreadPoolExecutor, as_completed, wait, ALL_COMPLETED
import copy
import random
import numpy
from dominio.Metaheuristics.NSGA_II import NsgaII
from dominio.Metaheuristics.GRASP import Grasp
from dominio.Solution import Solution
from conf import settings
from views.general_shift_view import GenerateShiftView
from utils.normalize import Normalize
import numpy as np
from utils.hipervolumen import Hipervolumen
from typing import List


def execute_ga(new_population, views, algorithm, num_weights, sol_per_pop, num_generations, num_parents_mating):
    # Defining the population size.
    # The population will have sol_per_pop chromosome where each chromosome has num_weights genes.
    pop_size = (sol_per_pop, num_weights)
    data = []
    dataSolutions = []
    for generation in range(num_generations-1):
        print("Generation"+ str(generation+1))
        # Measuring the fitness of each chromosome in the population.
        data_fitnesss = cal_pop_fitness(new_population, views, algorithm)
        fitness = data_fitnesss[0]
        data.append([new_population,fitness])
        dataSolutions.append(data_fitnesss[1])
        # Selecting the best parents in the population for mating.
        parents = select_mating_pool(new_population, fitness,num_parents_mating)

        # Generating next generation using crossover.
        offspring_crossover = crossover(parents,offspring_size=(pop_size[0]-parents.shape[0], num_weights))

        # Adding some variations to the offspring using mutation.
        offspring_mutation = mutation(offspring_crossover, algorithm ,  num_mutations = 2)

        # Creating the new population based on the parents and offspring.
        new_population[0:parents.shape[0], :] = parents
        new_population[parents.shape[0]:, :] = offspring_mutation
    # Getting the best solution after iterating finishing all generations.
    # At first, the fitness is calculated for each solution in the final generation.
    data_fitnesss = cal_pop_fitness(new_population, views, algorithm)
    fitness = data_fitnesss[0]
    data.append([new_population,fitness])
    dataSolutions.append(data_fitnesss[1])
    return data,dataSolutions


def cal_pop_fitness(population, views: List[GenerateShiftView], algorithm: str):
    # Calculating the fitness value of each solution in the current population.
    data = calculate_fitness_problem(population, views, algorithm)
    return numpy.array(data[0]),data[1]


def select_mating_pool(pop, fitness, num_parents):
    # Selecting the best individuals in the current generation as parents for producing the offspring of the next generation.
    parents = numpy.empty((num_parents, pop.shape[1]))
    fitnessCopy =  copy.copy(fitness)
    for parent_num in range(num_parents):
        max_fitness_idx = numpy.where(fitnessCopy == numpy.max(fitnessCopy))
        max_fitness_idx = max_fitness_idx[0][0]
        parents[parent_num, :] = pop[max_fitness_idx, :]
        fitnessCopy[max_fitness_idx] = -99999999999
    return parents


def crossover(parents, offspring_size):
    offspring = numpy.empty(offspring_size)
    #single point crossover
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
    # Mutation changes a number of genes as defined by the num_mutations argument. The changes are random.
    for idx in range(offspring_crossover.shape[0]):
        for mutation_num in range(num_mutations):
            gene_idx = random.randint(0,3)
            # The random value to be added to the gene.
            random_value = get_mutation_value(algorithm , mutation_num)
            offspring_crossover[idx, gene_idx] = offspring_crossover[idx,gene_idx] + random_value
    return offspring_crossover

def calculate_fitness_problem(population, views: List[GenerateShiftView], algorithm: str):
    max_iterations = 10    
    response = futureOptimizationResponses(population, views,algorithm,max_iterations)
    fitness = response[0]
    data = response[1]
    return fitness, data

def futureOptimizationResponses(population,views,algorithm,max_iterations):
    population_amount = len(population)
    responses = [0]  * population_amount
    data = []
    executor = ThreadPoolExecutor(max_workers=90)
    argsList = []
    for index,solution in enumerate(population):
        for view in views:
            argsList.append([solution,view,algorithm,max_iterations,index])
    futures = [executor.submit(executeAlgorithmToOptimize, args[0], args[1], args[2], args[3], args[4]) for args in argsList]
    for future in as_completed(futures):
        # get the result for the next completed task
        response = future.result()
        pos = response[1]
        value = response[0]
        responses[pos] = responses[pos] + value
        #Data,hv,index
        data.append((response[2],response[0],response[1]))
        print("NEW ITEM FINALIZADO")
        print(len(data))
    executor.shutdown() # blocks
    return responses,data
        
def executeAlgorithmToOptimize(solution: Solution, view: GenerateShiftView ,algorithm: str, max_iterations: int, index: int):
    data = []
    if algorithm == "GRASP":
        grasp = Grasp()
        grasp.setParameters(solution[0], solution[1], solution[2], solution[3])    
        population_amount = solution[3]         
        hv_average = 0
        MAX_TIME_DURATION = view.time
        for i in range(max_iterations):
            random.seed(settings.SEEDS[i])
            solutions = view.executeGraspToOptimize(grasp , population_amount, MAX_TIME_DURATION)
            solutionsNormalized = Normalize().normalizeFitness(solutions)
            pf = np.array(solutionsNormalized)
            hv = Hipervolumen.calculate_hipervolumen(pf)
            hv_average+= hv
            data.append((solutionsNormalized,hv))
    else:
        nsga = NsgaII()
        nsga.setParameters(solution[0], solution[1], solution[2], solution[3])
        population_amount = solution[3]         
        hv_average = 0
        MAX_TIME_DURATION = view.time
        for i in range(max_iterations):
            random.seed(settings.SEEDS[i])
            solutions = view.executeNsgaIIToOptimize(nsga, population_amount, MAX_TIME_DURATION)
            solutionsNormalized = Normalize().normalizeFitness(solutions)
            pf = np.array(solutionsNormalized)
            hv = Hipervolumen.calculate_hipervolumen(pf)
            hv_average+= hv
            data.append((solutionsNormalized,hv))
    return hv_average/max_iterations,index,data

def get_mutation_value(algorithm, mutation_num):
    if algorithm == "GRASP":
        #Components Amount
        if mutation_num == 0:
            return random.randrange(0, 21, 5)
        #Restricted List
        if mutation_num == 1:
            return random.randrange(0, 11, 2)
        #TweakAmountRepetion
        if mutation_num == 2:
            return random.randrange(0, 21, 5)
        #amount_population
        if mutation_num == 3:
            return random.randrange(0, 11, 5)
    else:    
        if mutation_num == 0:
            return numpy.random.randint(1, 2)
        if mutation_num == 1:
            return numpy.random.randint(1, 2)
        if mutation_num == 2:
            return numpy.random.randint(1, 5)
        if mutation_num == 3:
            return numpy.random.randint(1, 2)