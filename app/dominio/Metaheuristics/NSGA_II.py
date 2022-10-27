import copy
import time
from typing import List
from dominio.Algorithm import Algorithm
from dominio.Solution import Solution
from dominio.vigilant_assigment import VigilantAssigment
from dominio.population import Population
from services.population_services import PopulationServices
from conf import settings

class NsgaII(Algorithm):

    MAX_TIMEOUT: int
    MAX_EFOS: int = settings.MAX_EFOS_NSGAII   
    current_efo: int
    current_timeout: int

    POPULATION_AMOUNT_NSGAII = settings.POPULATION_AMOUNT_NSGAII

    evolutions: List[List[Solution]] = []

    
    def setParameters(self,children_amount_to_generate,amount_parents_of_ordered_population
    ,NUMBER_ITERATION_SELECTION_COMPONENTE, population_amount_nsgaii) -> None:
        self.MAX_EFOS = 99999999999999
        print("*********children_amount_to_generate", children_amount_to_generate)
        settings.NUMBER_OF_CHILDREN_GENERATE = int(children_amount_to_generate)
        settings.NUM_PARENTS_OF_ORDERED_POPULATION = amount_parents_of_ordered_population
        settings.NUMBER_ITERATION_SELECTION_COMPONENTE = int(NUMBER_ITERATION_SELECTION_COMPONENTE)
        self.POPULATION_AMOUNT_NSGAII = int(population_amount_nsgaii)

    def Execute(self, problem: VigilantAssigment, MAX_TIME_DURATION):
        self.CURRENT_TIMEOUT = time.time()
        self.MAX_TIMEOUT = self.CURRENT_TIMEOUT + MAX_TIME_DURATION
        self.current_efo = 1

        population_obj = Population(problem, self.POPULATION_AMOUNT_NSGAII)
        population_obj.inicialize_population(self.MAX_TIMEOUT)
        self.evolutions.append(population_obj.populations) 
        population_parents = [] 

        while self.current_efo < self.MAX_EFOS:
            self.CURRENT_TIMEOUT = time.time()
            if(self.CURRENT_TIMEOUT > self.MAX_TIMEOUT):
                return self.evolutions
            print(f"iteration N. {self.current_efo}")
            population_children = PopulationServices.generate_decendents(copy.deepcopy(population_obj)) 
            union_populantion = PopulationServices.union_soluction(copy.deepcopy(population_obj.populations), population_children)
            population_obj.populations = union_populantion
            PopulationServices.not_dominate_sort(population_obj) # return frent de pareto
            if not population_obj.populations:
                raise("population not found")
            PopulationServices.distance_crowding(population_obj)# order by population distance of crowding 
            rango = 1
            while population_obj.is_soluction_complete():
                range_of_solution = PopulationServices.get_solution_of_range(population_obj, rango)
                if range_of_solution:
                    population_parents=population_parents+range_of_solution
                else:
                   break 
                rango +=1
            population_obj.populations = population_parents
            population_obj.populations = population_obj.get_populations(self.POPULATION_AMOUNT_NSGAII)
            self.evolutions.append(population_obj.populations) 
            self.current_efo +=1
        return self.evolutions




























































































































