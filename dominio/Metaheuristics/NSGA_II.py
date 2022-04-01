import copy
from typing import List, Dict
from dominio.Algorithm import Algorithm
from utils.graph import Graph
from dominio.Solution import Solution
from dominio.vigilant_assigment import VigilantAssigment
# from dominio.soluction_nsga_ii import SoluctionNsgaII
from dominio.population import Population
from services.population_services import PopulationServices
from tests import generate_pyckle 


class NsgaII(Algorithm):
    CurrentEFOs: int = 0
    MaxEFOs: int = 10
    num_soluciones = 10
    num_decendents = 11

        

    def Execute(self, problem: VigilantAssigment):

        population_obj =  Population(problem, self.num_soluciones)
        population_obj.inicialize_population()
        # generate_pyckle.save_object("tests/population.pickle", population)
        # object = generate_pyckle.read_file('tests/population.pickle')
        population_parents: List[Solution] = population_obj.populations
        while self.CurrentEFOs < self.MaxEFOs:
            pulation_children = PopulationServices.generate_decendents(copy.copy(population_parents)) 
            union_populantion = PopulationServices.union_soluction(copy.copy(population_parents), pulation_children)
            population_obj.populations = union_populantion
            PopulationServices.not_dominate_sort(population_obj) # return frent de pareto
            population_parents = [] 
            PopulationServices.distance_crowding(population_obj)# order by population distance of crowding 
            rango = 1
            index_solution = 0
            while population_obj.is_soluction_complete():
                range_of_solution = PopulationServices.get_solution_of_range(population_obj, rango, index_solution)
                if range_of_solution:
                    population_parents.append(range_of_solution)
                else:
                   break 
                rango +=1
                index_solution +=1
            population_obj.populations = population_parents
            PopulationServices.not_dominate_sort(population_obj)
            Graph([population_obj.populations])
            return population_obj.get_Solutions_of_range(1)























































































































