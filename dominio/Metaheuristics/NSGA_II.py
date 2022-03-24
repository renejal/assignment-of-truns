import copy
from typing import List, Dict
from dominio.Algorithm import Algorithm
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
    # frentes: Dict[int,List[SoluctionNsgaII]]

        

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
            frente=population_obj.frente
            population_parents = [] 
            rango = 1
            while population_obj.is_soluction_complete(population_parents):
                # TODO: ESTUDIAR LA DIANTACIA DE CROWDING para continuar y terminal
                pass
                

            # cree una poblacion de Q de N hijos usando como operador de selección de padres el torneo
            # binario, cruece mutacion, cruece de punto etc y evalue los O objetivos de todos los hijos






















































































































