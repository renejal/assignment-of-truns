import copy
from typing import List
from conf import settings
from dominio.Solution import Solution
from dominio.Component import Component
from app.services.population_services import PopulationServices

class TweakVigilant:

    @classmethod
    def exchanges_vigilantes(self, parent_for_exchange_one: Solution, parent_for_exchange_two: Solution) -> List[Solution]:
        childrens: List[Solution] = []
        for i in range(settings.NUMBER_OF_CHILDREN_GENERATE):
            child = self.parent_crossing(copy.copy(parent_for_exchange_one),copy.copy(parent_for_exchange_two))
            if child:
                childrens.append(child)  
            elif childrens:
                PopulationServices.calculate_fitness(childrens)
                childrens = PopulationServices.get_best_Soluction(childrens, parent_for_exchange_one, parent_for_exchange_two)
        else:
            childrens.append(parent_for_exchange_one)
            childrens.append(parent_for_exchange_two)
        return childrens

    @classmethod
    def parent_crossing(parent_for_exchange_new: Solution, children: Solution) -> Solution:
        vigilants: List[Component] = PopulationServices.get_random_gens(copy.copy(parent_for_exchange_new),copy.copy(children)) #TODO: los vigilantes deven ser diferentes en las dos listas
        if not vigilants:
            return False
        for vigilant_new_id, vigilant_for_exchagen_id in zip(vigilants[0], vigilants[1]):
                children.crossing_vigilant(vigilant_new_id, vigilant_for_exchagen_id)
        return children