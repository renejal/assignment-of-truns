import imp
import copy
import random
from typing import List, Dict
# from msilib.schema import Component
from dominio.soluction_nsga_ii import SoluctionNsgaII
from dominio.Component import Component

class PopulationServices:

    @staticmethod
    def generate_decendents(population: List[SoluctionNsgaII], number_of_children: int) -> List[SoluctionNsgaII]:
        "a copy of tha populaton is received"
        childrens: list[SoluctionNsgaII] = []
        while len(population)>1:
            parents = PopulationServices.get_parents(population)
            childrens.append(PopulationServices.mating_between_parents(parents[0],parents[1], number_of_children))
        return childrens
    
    @staticmethod
    def get_parents(parents: List[SoluctionNsgaII]) -> List[SoluctionNsgaII]:
        response: List[SoluctionNsgaII] = []
        response.append(parents.pop(random.randint(0, len(parents)-1)))
        response.append(parents.pop(random.randint(0, len(parents)-1)))
        return response

    @staticmethod
    def mating_between_parents(parent_one: SoluctionNsgaII, parent_two: SoluctionNsgaII, number_of_children) -> SoluctionNsgaII:
        "maing between parent_one and parent"
        childrens: List[SoluctionNsgaII] = []
        for i in range(number_of_children):
            gen_parent_one: Component = parent_one.get_random_gen([])
            gen_parent_two: Component = parent_two.get_random_gen([gen_parent_one])
            childrens.append(PopulationServices.parent_crossing(parent_one, parent_two, gen_parent_one, gen_parent_two))  
        return PopulationServices.get_best_children(childrens)
        
    @staticmethod
    def get_best_children(childrens: List[SoluctionNsgaII]) -> SoluctionNsgaII:
        best: SoluctionNsgaII  = None
        for children in childrens:
            if best == None:
                best = children 
                continue
            if children.total_fitness > best.total_fitness:
                best = children
        return best

            
        pass
    @staticmethod
    def parent_crossing(children_one: SoluctionNsgaII, children_two: SoluctionNsgaII,
                        gen_parent_one: Component, gen_parent_two: Component) -> SoluctionNsgaII:
        children_one.mutation_component(gen_parent_two, gen_parent_one)
        children_one.reparate_component(gen_parent_two, gen_parent_one)
        children_two.mutation_component(gen_parent_one, gen_parent_two)
        children_two.reparate_component(gen_parent_two, gen_parent_one)
        return children_one, children_two

    @staticmethod
    def union_soluction(parents, children) -> List[SoluctionNsgaII]:
        """se encarda de unir los padres y los hijos de una misma lista y luego la ordena porn RANGO"""
        "return una lista unida de padres he hijos"
        return  parents + children

    def not_dominate_sort(population: List[SoluctionNsgaII])-> Dict[int,List[SoluctionNsgaII]]:
        population: List[SoluctionNsgaII]
        frentes: Dict[int,List[SoluctionNsgaII]]
        PopulationServices.calculate_soluction_dominated(population, frentes)
        PopulationServices.calculate_soluction_for_frentes(population, frentes)
        return frentes

    def calculate_soluction_for_frentes(self, soluction: SoluctionNsgaII, frentes: Dict[int, List[SoluctionNsgaII]]):
        range_soluction = 1
        while self.get_soluction_the_frente_whit_range(range_soluction):
            soluctions_of_range: List[SoluctionNsgaII] = self.get_soluction_the_frente_whit_range(range_soluction)
            for soluction_dominate in soluctions_of_range:
               for soluction in soluction_dominate.dominate: 
                    soluction.dominate_me -=1
                    if soluction.dominate_me == 0:
                        soluction.range += 1
                        self.add_frente(soluction, range_soluction+ 1)
            range_soluction += 1

        return frentes


    @staticmethod
    def calculate_soluction_dominated(population: List[SoluctionNsgaII], frente: List[SoluctionNsgaII]):

        for i in range(len(population)):
            population[i].dominate = [] # nueva lista vacia
            population[i].__dominate_me_account= 0 # numero de solucion que la dominan
            population[i].range_soluction = -1
            for j in range(len(population)):
                if i == j: continue
                if self.to_dominate(population[i],population[j]):
                    population[i].add_dominate(population[j].id)
                else:
                    if self.to_dominate(population[j],population[i]):
                        population[i].dominate_me += 1 #se incrementar le numero de soluciones que me dominar o domina a esta solucion
            if population[i].dominate_me == 0:
                population[i].range_soluction = 1
                self.add_frente(population[i],1, frente)

