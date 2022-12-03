from typing import List
from conf.settings import NUMBER_OBJECTIVE_AT_OBTIMIZATE, INFINITE_POSITIVE, INFINITE_NEGATIVE
from dominio.population import Population
from dominio.Solution import Solution
from nds import ndomsort
import copy
import random

class NonDominatedSorting:

    def getFronts(self, population: List[Solution]):
        ##TENER CUIDADO CON LAS SOLUCIOENS REPETIDAS POR AHORA VALIDAREMOS AQUI
        fitness = []
        solution_fronts = []
        for solution in population:
            fitnessess = [solution.fitness[0],solution.fitness[1],solution.fitness[2],solution.fitness[3]]
            if fitnessess not in fitness:
                fitness.append(fitnessess)
        fronts = ndomsort.non_domin_sort(fitness)
        for front in fronts:
            solutions_in_front = []
            for sol in fronts[front]:
                for solution in population:
                    if solution.fitness == sol:
                        solution.crowding_distance = 0
                        solution.range = front+1
                        solutions_in_front.append(solution)
                        break
            solution_fronts.append(solutions_in_front)
        return solution_fronts
    
    def get_best_populations(self, fronts: List[List[Solution]], amount_population):
        population = []
        for front in fronts:
            if len(population) == amount_population:
                return population
            if len(population) > amount_population:
                raise("MAL FARAMADA LA OBTENCION DE LA POBLACION!!!!!!!!!!!")
            if len(front) + len(population) < amount_population:
                population += front
            else:
                orderSolutins = self.distance_crowding(front)
                population+= orderSolutins[:amount_population - len(population)]
        return population
    def getFront(self, solutionsNormalized: List[List[int]]):
        fronts = ndomsort.non_domin_sort(solutionsNormalized)
        return fronts[0]

    def distance_crowding(self, frente: List[Solution]):
        rango = self.get_range_of_objective(frente)
        for j in range(NUMBER_OBJECTIVE_AT_OBTIMIZATE): # la lista de objetivos posiblemente se una lita de enteros 
            self.order_solution_of_objetive_value(frente, j)
            frente[0].crowding_distance = INFINITE_POSITIVE
            for i in range(1, len(frente)-1):
                value = (frente[i+1].fitness[j] - frente[i-1].fitness[j])
                if rango[j]!= 0:
                    value = value/rango[j]
                frente[i].crowding_distance += value
            frente[-1].crowding_distance = INFINITE_NEGATIVE
        soluciones = []
        for sol in frente:
            if sol.crowding_distance == INFINITE_POSITIVE or sol.crowding_distance == INFINITE_NEGATIVE:
                soluciones.append(sol)
        sol_in_middle = []
        for sol in frente:
            if sol.crowding_distance != INFINITE_POSITIVE and sol.crowding_distance != INFINITE_NEGATIVE:
                sol_in_middle.append(sol)
        sol_in_middle = sorted(sol_in_middle, key = lambda solution : solution.crowding_distance, reverse=True)
        soluciones+= sol_in_middle
        return soluciones

    def order_solution_of_objetive_value(self,population: List[Solution], index_objective, par_reverse=True):
        result = sorted(population, key = lambda solution : solution.fitness[index_objective], reverse=par_reverse) # reserve = True: ordena descendente
        return result

    def get_range_of_objective(self, frente: List[Solution]) -> List[int]:
        # para cada objetivo se calcula el max y el mix y se guarda el rango (max- min)
        # return list rangos, max y min por objetivo [[max-minx],[max,min]..]
        rango: List[int] = []
        min = INFINITE_POSITIVE
        max = INFINITE_NEGATIVE
        for index_objective in range(NUMBER_OBJECTIVE_AT_OBTIMIZATE):
            for solution in frente:
                if min > solution.fitness[index_objective]:
                    min = solution.fitness[index_objective]
                if max < solution.fitness[index_objective]:
                    max = solution.fitness[index_objective]
            rango.append(max-min)
        return rango