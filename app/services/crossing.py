
from typing import List
import random
from conf import settings
from dominio.Solution import Solution

class Crossing:

    @classmethod
    def get_parents_by_objetive(self, parents: List[Solution], objective_index) -> List[Solution]:
        population_order = self.order_solution_of_objetive_value(parents,objective_index,True) # order True: descendente
        num_solutions = int(len(population_order)* settings.NUM_PARENTS_OF_ORDERED_POPULATION)
        first_solutions = population_order[:num_solutions]
        end_solutions = population_order[-num_solutions:]
        parent_one = first_solutions.pop(random.randint(0, len(first_solutions)-1))
        parent_two = end_solutions.pop(random.randint(0, len(end_solutions)-1))
        return parent_one, parent_two
        
    @classmethod
    def order_solution_of_objetive_value(self, population: List[Solution], index_objective, par_reverse=True):
        result = sorted(population, key = lambda solution : solution.fitness[index_objective], reverse=par_reverse) # reserve = True: ordena descendente
        return result