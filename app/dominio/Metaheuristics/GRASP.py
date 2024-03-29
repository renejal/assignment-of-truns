import copy
import random
import time
from typing import List
from utils.non_dominated_sorting import NonDominatedSorting
from dominio.Algorithm import Algorithm
from dominio.Solution import Solution 
from dominio.population import Population
from dominio.vigilant_assigment import VigilantAssigment
from services.population_services import PopulationServices
from dominio.population import Population
from services.tweak_service import Tweak_service
from conf import settings

class Grasp(Algorithm):

    MAX_TIMEOUT: int
    MAX_EFOS: int = settings.MAX_EFOS_GRASP   
    current_efo: int
    current_timeout: int
    nonDominatedSorting = NonDominatedSorting()
    
    ALEATORY:int = 0 
    COMPONENTS_AMOUNT: int = settings.COMPONENTS_AMOUNT_GRASP
    RESTRICTED_LIST_AMOUNT_COMPONENT:int = settings.RESTRICTED_LIST_AMOUNT_COMPONENT_GRASP
    TWEAK_AMOUNT_REPETITIONS: int = settings.TWEAK_AMOUNT_REPETITIONS_GRASP
    AMOUNT_POPULATION: int = settings.POPULATION_AMOUNT_GRASP

    def setParameters(self,components_amount,restricted_list
    ,tweak_amount_repetitions, amount_population) -> None:
        self.MAX_EFOS = 99999999999999
        self.COMPONENTS_AMOUNT = components_amount
        if restricted_list >= components_amount:
            self.RESTRICTED_LIST_AMOUNT_COMPONENT = components_amount-1
        else:    
            self.RESTRICTED_LIST_AMOUNT_COMPONENT = restricted_list
        self.TWEAK_AMOUNT_REPETITIONS = tweak_amount_repetitions
        self.AMOUNT_POPULATION = amount_population

    def Execute(self, problem: VigilantAssigment , MAX_TIME_DURATION):
        self.current_efo = 1
        evolutions = []
        self.current_timeout = time.time()
        self.MAX_TIMEOUT = self.current_timeout + MAX_TIME_DURATION

        population: List[Solution] = self.get_initial_poblation(problem)
        evolutions.append(copy.deepcopy(population))
        if(self.current_timeout < self.MAX_TIMEOUT):
            while self.current_efo < self.MAX_EFOS:
                self.current_timeout = time.time()
                if(self.current_timeout > self.MAX_TIMEOUT):
                    return evolutions
                print("evolution:"+ str(self.current_efo+1))
                for index_solution in range(self.AMOUNT_POPULATION):
                    self.current_timeout = time.time()
                    if(self.current_timeout > self.MAX_TIMEOUT):
                        return evolutions
                    best_solution = self.local_optimization(population[index_solution])
                    population.append(best_solution)
                population = self.best_population(population)
                evolutions.append(copy.deepcopy(population))
                self.current_efo+= 1   
        return evolutions

    def get_initial_poblation(self,problem) -> List[Solution]:
        # print("Getting started population")
        population:List[Solution] = []
        for i in range(self.AMOUNT_POPULATION):
            S = Solution(problem)
            self.current_timeout = time.time()
            if(self.current_timeout > self.MAX_TIMEOUT):
                # print("timeout pass")
                return population
            while S.is_solution_complete():
                components = S.create_components(self.COMPONENTS_AMOUNT)
                restricted_list = S.get_best_components(components,self.RESTRICTED_LIST_AMOUNT_COMPONENT)
                S.merge_component(restricted_list)    
            population.append(S)
            print("new iteration")
        return population

    def local_optimization(self, actual_solution: Solution):
        best_solution:Solution = copy.deepcopy(actual_solution)
        for tweak_index in range(self.TWEAK_AMOUNT_REPETITIONS):
            self.current_timeout = time.time()
            if(self.current_timeout > self.MAX_TIMEOUT):
                break
            new_solution = Tweak_service().Tweak(copy.deepcopy(best_solution))
            if new_solution.total_fitness < best_solution.total_fitness:
                best_solution = new_solution
        return best_solution
        
    def best_population(self, population: List[Solution]) -> List[Solution]:
        newPopulation = self.nonDominatedSorting.getFronts(population)
        return self.nonDominatedSorting.get_best_populations(newPopulation,self.AMOUNT_POPULATION)
         

