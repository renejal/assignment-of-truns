import copy
from typing import List
from conf import settings
from dominio.Solution import Solution
from dominio.Component import Component
from services.crossing import Crossing
from dominio.population import Population

class CrossingVigilant:

    @classmethod
    def exchanges_vigilantes(self, parent_for_exchange_one: Solution, parent_for_exchange_two: Solution) -> List[Solution]:
        childrens: List[Solution] = []
        for i in range(settings.NUMBER_OF_CHILDREN_GENERATE):
            child = self.parent_crossing(copy.copy(parent_for_exchange_one),copy.copy(parent_for_exchange_two))
            if child:
                childrens.append(child)  
            elif childrens:
                self.calculate_fitness(childrens)
                childrens = self.get_best_Soluction(childrens, parent_for_exchange_one, parent_for_exchange_two)
        else:
            childrens.append(parent_for_exchange_one)
            childrens.append(parent_for_exchange_two)
        return childrens

    @classmethod
    def parent_crossing(self, parent_for_exchange_new: Solution, children: Solution) -> Solution:
        vigilants: List[Component] = self.get_random_gens(copy.copy(parent_for_exchange_new),copy.copy(children)) #TODO: los vigilantes deven ser diferentes en las dos listas
        if not vigilants:
            return False
        for vigilant_new_id, vigilant_for_exchagen_id in zip(vigilants[0], vigilants[1]):
                children.crossing_vigilant(vigilant_new_id, vigilant_for_exchagen_id)
        return children
    
    @classmethod
    def crossing_vigilantes(self, population: Population, objective_index=1) -> List[Solution]:
        parent_for_exchange_one, parent_for_exchange_two = Crossing.get_parents_by_objetive(population.populations, objective_index, settings)
        childrens: List[Solution] = []
        for i in range(settings.NUMBER_OF_CHILDREN_GENERATE):
            child = self.parent_crossing(copy.copy(parent_for_exchange_one),copy.copy(parent_for_exchange_two))
            if child:
                childrens.append(child)  
            elif childrens:
                self.calculate_fitness(childrens)
                childrens = self.get_best_Soluction(childrens, parent_for_exchange_one, parent_for_exchange_two)
        else:
            childrens.append(parent_for_exchange_one)
            childrens.append(parent_for_exchange_two)
        return childrens
        
    @classmethod
    def get_best_Soluction(self,childrens: List[Solution], parent_for_exchange_one: Solution, parent_for_exchange_two: Solution):
        for i in range(1):
            best = self.get_best_children_of_childrens_list(childrens)
            if best.total_fitness < (parent_for_exchange_one.total_fitness or parent_for_exchange_two.total_fitness):
                childrens.append(best)
        if len(childrens) == 1:
            best = parent_for_exchange_one if parent_for_exchange_one.total_fitness < parent_for_exchange_two.total_fitness else parent_for_exchange_two.total_fitness
            childrens.append(best)
        return childrens

    @classmethod
    def get_best_children_of_childrens_list(childrens: List[Solution]) -> Solution:
        best: Solution  = None
        for children in childrens:
            if best == None:
                best = children 
                continue
            if children.total_fitness > best.total_fitness:
                best = children
        childrens.remove(best)
        return best
    
    @classmethod
    def parent_crossing(self, parent_for_exchange_new: Solution, children: Solution) -> Solution:
        vigilants: List[Component] = self.get_random_gens(copy.copy(parent_for_exchange_new),copy.copy(children)) #TODO: los vigilantes deven ser diferentes en las dos listas
        if not vigilants:
            return False
        for vigilant_new_id, vigilant_for_exchagen_id in zip(vigilants[0], vigilants[1]):
                children.crossing_vigilant(vigilant_new_id, vigilant_for_exchagen_id)
        return children
    
    @classmethod
    def get_random_gens(self, parent_for_exchange_new: Solution, parent_for_exchange: Solution) -> List[Component]:
        "El metodo debe retornas la lista de vigilantes del componente y el componente del cual fue sacado"
        gen_parent_for_exchange_new: Component = None
        gen_parent_exchange: Component = None
        iteration = 0
        while iteration <= settings.NUMBER_ITERATION_SELECTION_COMPONENTE:
            gen_parent_for_exchange_new = parent_for_exchange_new.get_random_gen([])
            gen_parent_exchange = parent_for_exchange.get_random_gen([gen_parent_for_exchange_new.site_id])
            result = self.is_validation_and_repartion(gen_parent_for_exchange_new, gen_parent_exchange)
            if not result:
                return False
            if (result[0] and result[1]) != [] and (result[0] and result[1]) is not None:
                return result[0], result[1]
            iteration += 1
        return False
        raise("Error no se encontro vigilantes disponibles")

    @classmethod
    def is_validation_and_repartion(self, gen_new: Component, gen_exchange: Component): 
        vigilants_new: List[int] = [vigilant for vigilant in gen_new.assigned_Vigilantes]
        vigilants_exchange: List[int] = [vigilant for vigilant in gen_exchange.assigned_Vigilantes]

        if (vigilants_new and vigilants_exchange) == []:
            return None

        diference = list(set(vigilants_new) - set(vigilants_exchange))
        diference += list(set(vigilants_exchange) - set(vigilants_new))
        if not diference:
            return None
        vigilants_new_not_in_commont: List[int] = [vigilant for vigilant in gen_new.assigned_Vigilantes if vigilant in diference and gen_new.get_vigilant(vigilant).default_place_to_look_out == -1]
        vigilants_exchange_not_in_commont: List[int] = [vigilant for vigilant in gen_exchange.assigned_Vigilantes if vigilant in diference and gen_exchange.get_vigilant(vigilant).default_place_to_look_out == -1]
        return vigilants_new_not_in_commont, vigilants_exchange_not_in_commont
    
    classmethod
    def calculate_fitness(self,childrens: List[Solution]):
        for children in childrens:
            children.calculate_fitness()