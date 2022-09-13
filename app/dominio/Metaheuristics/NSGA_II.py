import copy
from typing import List
from dominio.Algorithm import Algorithm
from utils.graph import Graph
from dominio.Solution import Solution
from dominio.vigilant_assigment import VigilantAssigment
# from dominio.soluction_nsga_ii import SoluctionNsgaII
from dominio.population import Population
from services.population_services import PopulationServices
from tests import generate_pyckle 
from conf import settings
# generate_pyckle.save_object("tests/population.pickle", population)
# object = generate_pyckle.read_file('tests/population.pickle')

class NsgaII(Algorithm):
    currency_efos = 0
    Evoluction_soluction: List[List[Solution]]= []

    
    def setParameters(self,children_amount_to_generate,amount_parents_of_ordered_population
    ,tweak_amount_repetitions, amount_population) -> None:
    #TODO cambiar semilla
        self.CHILDREN_AMOUNT_TO_GENERATE = children_amount_to_generate
        self.AMOUNT_PARENTS_OF_ORDERED_POPULATION = amount_parents_of_ordered_population
        self.TWEAK_AMOUNT_REPETITIONS = tweak_amount_repetitions
        self.AMOUNT_POPULATION = amount_population


    def Execute(self, problem: VigilantAssigment):
        population_obj =  Population(problem, settings.NUM_SOLUTION)
        population_obj.inicialize_population()
        while self.currency_efos < settings.MAX_EFOS:
            #TODO BREAK TIMER
            print(f"iteration N. {self.currency_efos}")
            population_parents: List[Solution] = population_obj.populations
            population_children = PopulationServices.generate_decendents(copy.copy(population_parents)) 
            union_populantion = PopulationServices.union_soluction(copy.copy(population_parents), population_children)
            population_obj.populations = union_populantion
            PopulationServices.not_dominate_sort(population_obj) # return frent de pareto
            population_parents = [] 
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
            population_obj.populations = population_obj.get_populations(settings.AMOUNT_POBLATION_TO_CREATE)
            self.Evoluction_soluction.append(population_obj.populations) 
            self.currency_efos +=1
        return self.Evoluction_soluction




























































































































