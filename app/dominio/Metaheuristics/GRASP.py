import copy
import random
import time
from typing import List

from dominio.Algorithm import Algorithm
from dominio.Solution import Solution 
from dominio.population import Population
from dominio.vigilant_assigment import VigilantAssigment
from services.population_services import PopulationServices
from dominio.population import Population
from services.tweak_service import Tweak_service
from conf.settings import AMOUNT_POPULATION_TO_CREATE

class Grasp(Algorithm):

    MAX_TIMEOUT: int
    CURRENT_TIMEOUT: int

    #TODO max efos cambiarlo por tiempo.
    
    ALEATORY:int = 0
    CURRENT_EFOS: int = 0
    MAX_EFOS: int = 10
    
    COMPONENTS_AMOUNT: int = 50
    RESTRICTED_LIST_AMOUNT_COMPONENT:int = 10
    TWEAK_AMOUNT_REPETITIONS: int = 10
    AMOUNT_POPULATION: int = AMOUNT_POPULATION_TO_CREATE

    def setParameters(self,components_amount,restricted_list
    ,tweak_amount_repetitions, amount_population) -> None:
    #TODO cambiar semilla
        self.COMPONENTS_AMOUNT = components_amount
        if restricted_list >= components_amount:
            self.RESTRICTED_LIST_AMOUNT_COMPONENT = components_amount-1
        else:    
            self.RESTRICTED_LIST_AMOUNT_COMPONENT = restricted_list
        self.TWEAK_AMOUNT_REPETITIONS = tweak_amount_repetitions
        self.AMOUNT_POPULATION = amount_population

    def Execute(self, problem: VigilantAssigment):
        fig = None
        self.CURRENT_EFOS = 0
        data = []
        self.CURRENT_TIMEOUT = time.time()
        self.MAX_TIMEOUT = self.CURRENT_TIMEOUT + 10

        population: List[Solution] = self.get_initial_poblation(problem)
        if(self.CURRENT_TIMEOUT < self.MAX_TIMEOUT):
            while self.CURRENT_EFOS < self.MAX_EFOS:
                self.CURRENT_TIMEOUT = time.time()
                if(self.CURRENT_TIMEOUT > self.MAX_TIMEOUT):
                    return population, fig
                print("evolution:"+ str(self.CURRENT_EFOS+1))
                for index_solution in range(self.AMOUNT_POPULATION):
                    self.CURRENT_TIMEOUT = time.time()
                    if(self.CURRENT_TIMEOUT > self.MAX_TIMEOUT):
                        return population, fig
                    new_solution:Solution = copy.deepcopy(population[index_solution])
                    for tweak_index in range(self.TWEAK_AMOUNT_REPETITIONS):
                        self.CURRENT_TIMEOUT = time.time()
                        if(self.CURRENT_TIMEOUT > self.MAX_TIMEOUT):
                            break
                        new_solution = Tweak_service().Tweak(new_solution)
                    population.append(new_solution)
                data.append(population)
                population = self.best_population(population)
                self.CURRENT_EFOS+=1   
        return data

    def get_initial_poblation(self,problem) -> List[Solution]:
<<<<<<< HEAD
        print("Getting started population")
        population:List[Solution] = []
        for i in range(self.AMOUNT_POPULATION):
=======
        poblation:List[Solution] = []
        for i in range(self.AMOUNT_POBLATION):
>>>>>>> fb59b2d362de5153e8c710200048b1229ddd1e8e
            S = Solution(problem)
            self.CURRENT_TIMEOUT = time.time()
            if(self.CURRENT_TIMEOUT > self.MAX_TIMEOUT):
                print("timeout pass")
                return population
            while S.is_solution_complete():
                components = S.create_components(self.COMPONENTS_AMOUNT)
<<<<<<< HEAD
                restricted_list = S.get_best_components(components,self.RESTRICTED_LIST_AMOUNT_COMPONENT)
                S.merge_component(restricted_list)    
            population.append(S)
            print("new iteration")
        return population
=======
                restricted_list = components
                if restricted_list == None:
                    continue
                else:
                    best_restricted_list = S.get_best_components(restricted_list,self.RESTRICTED_LIST_AMOUNT_COMPONENT)
                    S.merge_component(best_restricted_list)    
            poblation.append(S)
        return poblation
>>>>>>> fb59b2d362de5153e8c710200048b1229ddd1e8e

    def best_population(self, population: List[Solution]) -> List[Solution]:
        #TODO ordenamiento no dominadoa
        PopulationServices.not_dominate_sort(Population(None, None, population))
        population = PopulationServices.get_solutions_by_frente(population,len(population)/2)
        return population

