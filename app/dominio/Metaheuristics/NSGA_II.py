import copy
import time
from typing import List
from utils.non_dominated_sorting import NonDominatedSorting
from dominio.Algorithm import Algorithm
from dominio.Solution import Solution
from dominio.vigilant_assigment import VigilantAssigment
from dominio.population import Population
from services.population_services import PopulationServices
from conf import settings

class NsgaII(Algorithm):

    nonDominatedSorting = NonDominatedSorting()

    MAX_TIMEOUT: int
    MAX_EFOS: int = settings.MAX_EFOS_NSGAII   
    current_efo: int
    current_timeout: int

    POPULATION_AMOUNT_NSGAII = settings.POPULATION_AMOUNT_NSGAII

    evolutions: List[List[Solution]] = []

    
    def setParameters(self,children_amount_to_generate,amount_parents_of_ordered_population
    ,NUMBER_ITERATION_SELECTION_COMPONENTE, population_amount_nsgaii) -> None:
        self.MAX_EFOS = 99999999999999
        settings.NUMBER_OF_CHILDREN_GENERATE = int(children_amount_to_generate)
        settings.NUM_PARENTS_OF_ORDERED_POPULATION = amount_parents_of_ordered_population
        settings.NUMBER_ITERATION_SELECTION_COMPONENTE = int(NUMBER_ITERATION_SELECTION_COMPONENTE)
        self.POPULATION_AMOUNT_NSGAII = int(population_amount_nsgaii)

    def Execute(self, problem: VigilantAssigment, MAX_TIME_DURATION):
        self.CURRENT_TIMEOUT = time.time()
        self.MAX_TIMEOUT = self.CURRENT_TIMEOUT + MAX_TIME_DURATION
        self.current_efo = 1

        print("START NSGA")
        population_obj = Population(problem, self.POPULATION_AMOUNT_NSGAII)
        population_obj.inicialize_population(self.MAX_TIMEOUT)
        self.evolutions.append(copy.deepcopy(population_obj.populations)) 

        while self.current_efo < self.MAX_EFOS:
            try:
                self.CURRENT_TIMEOUT = time.time()
                if(self.CURRENT_TIMEOUT > self.MAX_TIMEOUT):
                    return self.evolutions
                print(f"iteration N. {self.current_efo}, time: {self.MAX_TIMEOUT - self.CURRENT_TIMEOUT}")
                population_children = PopulationServices.generate_decendents(copy.deepcopy(population_obj)) 
                union_populantion = PopulationServices.union_soluction(population_obj.populations, population_children)
                newPopulation = self.best_population(union_populantion)
                self.evolutions.append(copy.deepcopy(newPopulation)) 
                population_obj.populations = newPopulation
            except:
                print("ERROR")
                self.delete_error(population_obj.populations)
                continue
            self.current_efo +=1
        self.delete_error(population_obj.populations)
        return self.evolutions

    def delete_error(self,  population: List[Solution]):
        i = 0
        print("ERROR")
        while i < len(population):
            if not isinstance(population[i],Solution):
                print("se removio", population[i])
                population.remove(population[i])
            i = i + 1

    def best_population(self, population: List[Solution]) -> List[Solution]:
        newPopulation = self.nonDominatedSorting.getFronts(population)
        return self.nonDominatedSorting.get_best_populations(newPopulation,self.POPULATION_AMOUNT_NSGAII)
            

            




























































































































