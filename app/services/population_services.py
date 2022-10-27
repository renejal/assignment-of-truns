import random
from conf import settings
from typing import List
from dominio.model.vigilant import Vigilant
from dominio.population import Population
from dominio.Solution import Solution
from dominio.Solution import Solution
from dominio.Component import Component
from services.crossing_shift import CrossingShift
from services.crossing_vigilant import CrossingVigilant
from conf.settings import (MISSING_SHIFT_CROSSING_PROBABILITY, 
                           ASSIGNED_VIGILANTES_CROSSING_PROBABILITY, 
                           EXTRA_HOURS_CROSSING_PROBABILITY,
                           DISTANCE_CROSSING_PROBABILITY,
                           NUMBER_OBJECTIVE_AT_OBTIMIZATE
                           )


class PopulationServices:

    @staticmethod
    def generate_decendents(population: Population) -> List[Solution]:
        print("generate_decendents")
        childrens: list[Solution] = []
        PopulationServices.add_ids_solution(population.populations)
        while len(childrens)<len(population.populations): 
            function_crossing = PopulationServices.get_crossing()
            childrens = childrens + function_crossing(population)
        return childrens

    @staticmethod
    def get_crossing():
        #Todo: esta cambiando el random, revisar
        objective = random.choices([2,2,2,2], weights = (MISSING_SHIFT_CROSSING_PROBABILITY,
                                                          ASSIGNED_VIGILANTES_CROSSING_PROBABILITY,
                                                          EXTRA_HOURS_CROSSING_PROBABILITY,
                                                          DISTANCE_CROSSING_PROBABILITY))[0]
        objective = 2 # Todo quieta esto, solo es apra probar el crossing 3
        objective_dict ={
            1:CrossingShift.crossing_missing_shift,
            2:CrossingShift.crossing_vigilant_assigment,
            3:CrossingShift.crossing_hours_extras,
            4:CrossingVigilant.crossing_vigilantes
            }
        return objective_dict.get(objective)

    def remove_vigilants_default_the_site(gen: Component):
        Vigilants: List[Vigilant] = gen.assigned_Vigilantes
        index_vigilant = 0
        while index_vigilant < len(index_vigilant):
            vigilant = Vigilants[index_vigilant]
            if vigilant.default_place_to_look_out == -1:
                Vigilants.remove(vigilant)
                continue
            index_vigilant+=1

    @staticmethod
    def union_soluction(parents, childrens: List[Solution]) -> List[Solution]:
        print("union_soluction")
        for children in childrens:
            pass
            # print("fitness antes A", children.fitness[3])
            # print("fitness antes B", children.fitness[3])
            # children.recalculate_fitness()
            # print("fitness despues A", children.fitness[3])
            # print("fitness despues B", children.fitness[3])
        return  parents + childrens
    
    @staticmethod
    def to_dominate(soluction_one: Solution, soluction_two: Solution)-> bool:
        response = False
        number_of_objetives = len(soluction_one.fitness)
        for j in range(number_of_objetives):
            if soluction_one.fitness[j] < soluction_two.fitness[j]:
                response = True
            else:
                if soluction_two.fitness[j] < soluction_one.fitness[j]:
                    return False
        return response

    @staticmethod
    def not_dominate_sort(population: Population) -> List[Solution]:
        PopulationServices.add_ids_solution(population.populations)
        PopulationServices.calculate_dominance(population)
        PopulationServices.calculate_range(population)
        return population.frente

    @staticmethod
    def add_ids_solution(population: List[Solution]):
        try:
            for index, solution in enumerate(population):
                solution.id = index + 1
        except:
            raise("error population",population)

    @staticmethod
    def calculate_range(population: Population):
        rango = 1
        while population.frente.get(rango): # rango 1 del frente de pareto
            solutions: List[Solution] = population.frente.get(rango)
            for dominated_solution in solutions:
               for solution_id in dominated_solution.dominated:
                    solution = PopulationServices.get_solution(population.populations,solution_id)
                    if not solution: break # no ecuentra la solution 5
                    solution.dominate_me -=1
                    if solution.dominate_me == 0:
                        r=rango+1
                        solution.range=r 
                        population.add_frente(key=rango,value=solution)
            rango +=1
            
    @staticmethod
    def get_solution(population: List[Solution], id_solution: int):
        for solution in population:
            if solution.id == id_solution:
                return solution
        return False

    @staticmethod
    def get_frente(population: List[Solution], range):
        frente: List[Solution] = []
        for solution in population:
            if solution.range == range:
                frente.append(solution)
        return frente 

    @staticmethod
    def get_solutions_by_frente(population: List[Solution], amount:int):
        frente: List[Solution] = []
        if len(population) < amount:
            amount = len(population)
        range = 1
        while len(frente) < amount:
            for solution in population:
                if solution.range == range:
                    frente.append(solution)
                    if len(frente) == amount:
                        return frente
            range+=1 
        return frente

    @staticmethod
    def calculate_dominance(population_object: Population):
        population = population_object.populations
        for i in range(len(population)):
            population[i].dominated=[] # nueva lista vacia
            population[i].__dominate_me_account= 0 # numero de solucion que la dominan
            population[i].range= -1
            for j in range(len(population)):
                if i == j: continue
                if PopulationServices.to_dominate(population[i],population[j]): # la solucion i domina a la solucion j ?
                    population[i].add_dominate(population[j].id)
                else:
                    if PopulationServices.to_dominate(population[j],population[i]):
                        population[i].dominate_me += 1 #se incrementar le numero de soluciones que me dominar o domina a esta solucion
            if population[i].dominate_me == 0:
                population[i].range= 1
                population_object.add_frente(key=1,value=population[i])
    
    def distance_crowding(population: Population):
        frente = population.populations
        rango = PopulationServices.get_range_of_objective(frente)
        for solution in frente:
            solution.crowding_distance = 0
        for j in range(NUMBER_OBJECTIVE_AT_OBTIMIZATE): # la lista de objetivos posiblemente se una lita de enteros 
            PopulationServices.order_solution_of_objetive_value(frente, j)
            frente[0].crowding_distance = settings.INFINITE_POSITIVE
            for i in range(1, len(frente)-1):
                value = (frente[i+1].fitness[j] - frente[i-1].fitness[j])
                if rango[j]!= 0:
                   value = value/rango[j]
                frente[i].crowding_distance += value
            frente[-1].crowding_distance = settings.INFINITE_NEGATIVE
    
    def get_range_of_objective(frente: List[Solution]) -> List[int]:
        # para cada objetivo se calcula el max y el mix y se guarda el rango (max- min)
        # return list rangos, max y min por objetivo [[max-minx],[max,min]..]
        rango: List[int] = []
        min = settings.INFINITE_POSITIVE
        max = settings.INFINITE_NEGATIVE
        for index_objective in range(settings.NUMBER_OBJECTIVE_AT_OBTIMIZATE):
            for solution in frente:
                if min > solution.fitness[index_objective]:
                    min = solution.fitness[index_objective]
                if max < solution.fitness[index_objective]:
                    max = solution.fitness[index_objective]
            rango.append(max-min)
        return rango

    @staticmethod
    def get_solution_of_range(population: Population, range: int):
        "return soluction of range x"
        soluctions = population.get_Solutions_of_range(range)
        if soluctions:
            return soluctions
        else:
            return soluctions
        
    @staticmethod
    def order_solution_of_objetive_value(population: List[Solution], index_objective, par_reverse=True):
        result = sorted(population, key = lambda solution : solution.fitness[index_objective], reverse=par_reverse) # reserve = True: ordena descendente
        return result

    
        

