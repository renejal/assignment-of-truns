import imp
import copy
import random
from re import I
from urllib import response
from conf import settings 
from typing import List, Dict, Tuple
from dominio.model.vigilant import Vigilant
# from msilib.schema import Component
from dominio.soluction_nsga_ii import SoluctionNsgaII
from dominio.Component import Component
from services.tweak_assignment_vigilantes_amount import Tweak_assignment_vigilantes_amount

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
    def mating_between_parents(parent_for_exchange_one: SoluctionNsgaII, parent_for_exchange_two: SoluctionNsgaII, number_of_children) -> SoluctionNsgaII:
        "maing between parent_one and parent"
        childrens: List[SoluctionNsgaII] = []
        for i in range(number_of_children):
            childrens.append(PopulationServices.parent_crossing(copy.copy(parent_for_exchange_one),copy.copy(parent_for_exchange_two)))  
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

    def remove_vigilants_default_the_site(gen: Component):
        Vigilants: List[Vigilant] = gen.assigned_Vigilantes
        for vigilant in Vigilants:
            if vigilant.default_place_to_look_out == -1:
                Vigilants.remove(vigilant)
        
    @staticmethod
    def is_validation_and_repartion(gen_new: Component, gen_exchange: Component): 
        """retorna true si se encontro vigilantes no por default y distintos entre los dos genes"""
        vigilants_new: List[int] = [vigilant.id for vigilant in gen_new.assigned_Vigilantes if vigilant.default_place_to_look_out == -1]
        vigilants_exchange: List[int] = [vigilant.id for vigilant in gen_exchange.assigned_Vigilantes if vigilant.default_place_to_look_out == -1]
        vigilants_new_not_in_commont: List[int] = [vigilant_id for vigilant_id in vigilants_new if vigilant_id not in vigilants_exchange]
        vigilants_exchange_not_in_commont: List[int] = [vigilant_id for vigilant_id in vigilants_exchange if vigilant_id not in vigilants_new]
        return vigilants_new_not_in_commont, vigilants_exchange_not_in_commont

    @staticmethod
    def get_random_gens(parent_for_exchange_new: SoluctionNsgaII, parent_for_exchange: SoluctionNsgaII) -> List[Component]:
        "El metodo debe retornas la lista de vigilantes del componente y el componente del cual fue sacado"
        gen_parent_for_exchange_new: Component = None
        gen_parent_exchange: Component = None
        iteration = 0
        while iteration <= settings.NUMBER_ITERATION_SELECTION_COMPONENTE:
            gen_parent_for_exchange_new = parent_for_exchange_new.get_random_gen([])
            gen_parent_exchange = parent_for_exchange.get_random_gen([gen_parent_for_exchange_new])
            vigilants_new, vigilants_exchanges = PopulationServices.is_validation_and_repartion(gen_parent_for_exchange_new, gen_parent_exchange)
            if (vigilants_new and vigilants_exchanges) != []:
                return [vigilants_new, vigilants_exchanges]
            iteration += 1
        raise("Error no se encontro vigilantes disponibles")

    @staticmethod
    #todo debe resibir una copia de los parametros
    def parent_crossing(parent_for_exchange_new: SoluctionNsgaII, children: SoluctionNsgaII) -> SoluctionNsgaII:
        "el hijo va hacer  una copia de la nueva solucion con su respectiva mutacion"
        vigilants: List[Component] = PopulationServices.get_random_gens(copy.copy(parent_for_exchange_new),copy.copy(children)) #TODO: los vigilantes deven ser diferentes en las dos listas
        for vigilant_new_id, vigilant_for_exchagen_id in zip(vigilants[0], vigilants[1]):
                children.crossing_vigilant(vigilant_new_id, vigilant_for_exchagen_id)
                children.reparate_soluction(vigilant_new_id, vigilant_for_exchagen_id)
        return children

    @staticmethod
    def union_soluction(parents, children) -> List[SoluctionNsgaII]:
        """se encarda de unir los padres y los hijos de una misma lista y luego la ordena porn RANGO"""
        "return una lista unida de padres he hijos"
        return  parents + children
    
    @staticmethod
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

