import random
from typing import List
from conf import settings
from utils.order import Order
from dominio.Solution import Solution

class Crossing:

    @classmethod
    def get_parents_by_objetive(self, parents: List[Solution], objective_index, settings) -> List[Solution]:
        """" obtiene los padres a crusar

        Args:
            parents (List[Solution]): soluciones a crusar
            objective_index (_type_): criterio de ordenacion 

        Returns:
            List[Solution]: parent_one : mejor solucion con respecto al fitnnes
            List[Solution]: parent_two : peor solucion con respecto al fitnnes
        """
        population_order = self.order_solution_of_objetive_value(parents,objective_index,True) # order True: descendente
        num_solutions = int(len(population_order)* settings.NUM_PARENTS_OF_ORDERED_POPULATION)
        if num_solutions == 0: num_solutions = 1
        first_solutions = population_order[:num_solutions]
        end_solutions = population_order[-num_solutions:]
        parent_one = first_solutions.pop(random.randint(0, len(first_solutions)-1))
        parent_two = end_solutions.pop(random.randint(0, len(end_solutions)-1))
        return parent_one, parent_two
        
    @classmethod 
    def get_best_parent(self, populations: List[Solution], objective_index) -> Solution:
        """" obtiene los padres a crusar

        Args:
            parents (List[Solution]): soluciones a crusar
            objective_index (_type_): criterio de ordenacion 

        Returns:
            List[Solution]: solucion: Rango de mejores soluciones 
        """
        population_order = self.order_solution_of_objetive_value(populations,objective_index,False) # order True: descendente
        parent = Order.list_restricted(population_order,1,settings.NUM_PARENTS_OF_ORDERED_POPULATION)
        print("lenParent", len(parent))
        return parent[0]

    @classmethod
    def order_solution_of_objetive_value(self, population: List[Solution], index_objective, par_reverse=True):
        result = sorted(population, key = lambda solution : solution.fitness[index_objective], reverse=par_reverse) # reserve = True: ordena descendente
        return result