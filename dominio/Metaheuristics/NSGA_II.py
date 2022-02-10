import copy
from typing import List, Dict
from dominio.Algorithm import Algorithm
from dominio.vigilant_assigment import VigilantAssigment
from dominio.soluction_nsga_ii import SoluctionNsgaII
from dominio.population import Population
from services.population_services import PopulationServices


class NsgaII(Algorithm):
    CurrentEFOs: int = 0
    MaxEFOs: int = 10
    num_soluciones = 10
    num_decendents = 11
    frentes: Dict[int,List[SoluctionNsgaII]]

    def Execute(self, problem: VigilantAssigment):

        population =  Population(problem, self.num_soluciones)
        population_parents: List[SoluctionNsgaII] = population.populations
        while self.CurrentEFOs < self.MaxEFOs:
            pulation_children = PopulationServices.generate_decendents(copy.copy(population_parents), self.num_decendents) 
            union_populantion = PopulationServices.union_soluction(population_parents, pulation_children)
            self.frente = PopulationServices.not_dominate_sort(union_populantion) # return frent de pareto
            population_parents = [] 
            rango = 1
            while population.is_soluction_complete(population_parents):
                # TODO: ESTUDIAR LA DIANTACIA DE CROWDING para continuar y terminal
                pass
                

            # cree una poblacion de Q de N hijos usando como operador de selección de padres el torneo
            # binario, cruece mutacion, cruece de punto etc y evalue los O objetivos de todos los hijos






















































































































