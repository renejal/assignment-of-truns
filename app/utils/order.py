from typing import List
from dominio.Component import Component
class Order:

    @classmethod
    def order_solution_of_objetive_value(self, population, index_objective, par_reverse=True):
        result = sorted(population, key = lambda solution : solution.fitness[index_objective], reverse=par_reverse) # reserve = True: ordena descendente
        return result

    @classmethod
    def order_sitio_of_objective_value(self, components: List[Component], fitnessToOptimize, par_reverse=True) -> Component:
        result = sorted(components, key = lambda component : component.get_fitness_by_criteria(fitnessToOptimize), reverse=par_reverse) # reserve = True: ordena descendente
        return result
    