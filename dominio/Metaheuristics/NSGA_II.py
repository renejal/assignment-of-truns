import copy
from typing import List
from dominio.Algorithm import Algorithm
from dominio.vigilant_assigment import VigilantAssigment
from dominio.soluction_nsga_ii import SoluctionNsgaII
from dominio.population import Population

class NsgaII(Algorithm):
    CurrentEFOs: int = 0
    MaxEFOs: int = 10
    num_soluciones = 10
    num_decendents = 11

    def Execute(self, problem: VigilantAssigment):
        P: List[SoluctionNsgaII] = []
        population: List[SoluctionNsgaII] = []
        population_service = Population()
        parents = population_service.inicialize_population(problem, self.num_soluciones)
        while self.CurrentEFOs < self.MaxEFOs:
            children = population_service.generate_decendents(parents, self.num_decendents)
            population = population_service.union_soluction(parents, children)
            population = population_service.not_dominate_sort(population)
            parents = None # rango = 1
            for i in range(len(population)):
                pass
                

            # cree una poblacion de Q de N hijos usando como operador de selección de padres el torneo
            # binario, cruece mutacion, cruece de punto etc y evalue los O objetivos de todos los hijos






















































































































