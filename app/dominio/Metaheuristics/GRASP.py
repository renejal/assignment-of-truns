import copy
import random
from typing import List

from dominio.Algorithm import Algorithm
from dominio.Solution import Solution 
from dominio.population import Population
from dominio.vigilant_assigment import VigilantAssigment
from services.population_services import PopulationServices
from dominio.population import Population
from services.tweak_service import Tweak_service
from utils.graph import Graph

class Grasp(Algorithm):
    ALEATORY:int = 0
    CURRENT_EFOS: int = 0
    MAX_EFOS: int = 10
    # COMPONENTS_AMOUNT: int = 300
    COMPONENTS_AMOUNT: int = 50
    # RESTRICTED_LIST_AMOUNT_COMPONENT:int = 15
    RESTRICTED_LIST_AMOUNT_COMPONENT:int = 5
    TWEAK_AMOUNT_REPETITIONS: int = 10
    AMOUNT_POBLATION: int = 5

    def Execute(self, problem: VigilantAssigment):
        Best = None
        data = []
        # poblation: List[Solution] = self.get_initial_poblation(problem)
        population = Population(None, None, self.get_initial_poblation(problem))
        while self.CURRENT_EFOS < self.MAX_EFOS:
            print("evolution:"+ str(self.CURRENT_EFOS+1))
            for index_solution in range(self.AMOUNT_POBLATION):
                new_solution:Solution = copy.deepcopy(population.populations[index_solution])
                for tweak_index in range(self.TWEAK_AMOUNT_REPETITIONS):
                    tweak = random.randint(1,4)      
                    new_solution = Tweak_service().Tweak(new_solution,tweak)
                population.populations.append(new_solution)
            data.append(population.populations)
            best = self.best_population(population)
            self.CURRENT_EFOS+=1   
        Graph(data)
        return best 

    def get_initial_poblation(self,problem) -> List[Solution]:
        print("Getting started poblation")
        poblation:List[Solution] = []
        for i in range(self.AMOUNT_POBLATION):
            S = Solution(problem, self.ALEATORY)
            while S.is_solution_complete():
                components = S.create_components(self.COMPONENTS_AMOUNT)
                restricted_list = components
                if restricted_list == None:
                    continue
                else:
                    best_restricted_list = S.get_best_components(restricted_list,self.RESTRICTED_LIST_AMOUNT_COMPONENT)
                    S.merge_component(best_restricted_list)    
            poblation.append(S)
            print("new iteration")
        return poblation

    def best_population(self, population: Population) -> List[Solution]:
        #TODO ordenamiento no dominadoa
        PopulationServices.not_dominate_sort(population)
        population.populations = PopulationServices.get_frente(population.populations,1)
        return population.populations
        # newpoblation = []
        # while len(newpoblation) != self.AMOUNT_POBLATION:
        #     rand = random.randint(0,self.AMOUNT_POBLATION*2)
        #     solution = population.populations[rand-1]
        #     if solution not in newpoblation:
        #         newpoblation.append(solution)
        # return newpoblation

