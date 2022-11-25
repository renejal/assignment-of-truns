from typing import List
from dominio.population import Population
from dominio.Solution import Solution
from nds import ndomsort
import copy

class NonDominatedSorting:

    def getFronts(self, population: List[Solution], amount_poblation):
        solutions = copy.deepcopy(population)
        fitness = []
        order_solutions = []
        final_solutions = []
        for solution in solutions:
            fitness.append([solution.fitness[0],solution.fitness[1],solution.fitness[2],solution.fitness[3]])
        fronts = ndomsort.non_domin_sort(fitness)

        # Or we can get values of objectives.
        # fronts = ndomsort.non_domin_sort(seq, lambda x: x[:2])

        # 'fronts' is a tuple of front's indices, not a dictionary.
        # fronts = ndomsort.non_domin_sort(seq, only_front_indices=True)
        for front in fronts:
            for seq in fronts[front]:
                order_solutions.append(seq)
                if(amount_poblation <= len(order_solutions)):
                    break

            if(amount_poblation <= len(order_solutions)):
                    break
        for order_solution in order_solutions:
             for solution in solutions:
                if (solution.fitness == order_solution):
                    final_solutions.append(solution)
                    break
        return final_solutions
    
    def getFrontsNSGA(population: Population, amount_poblation) -> List[Solution]:
        pop = copy.copy(population)
        fitness = []
        order_solutions = []
        final_solutions = []
        for solution in pop.populations:
            fitness.append([solution.fitness[0],solution.fitness[1],solution.fitness[2],solution.fitness[3]])
        fronts = ndomsort.non_domin_sort(fitness)

        # Or we can get values of objectives.
        # fronts = ndomsort.non_domin_sort(seq, lambda x: x[:2])

        # 'fronts' is a tuple of front's indices, not a dictionary.
        # fronts = ndomsort.non_domin_sort(seq, only_front_indices=True)
        # for front in fronts:
        #     for seq in fronts[front]:
        #         order_solutions.append(seq)
        #         if(amount_poblation <= len(order_solutions)):
        #             break

        #     if(amount_poblation <= len(order_solutions)):
        #             break
        # for order_solution in order_solutions:
        #      for solution in solutions:
        #         if (solution.fitness == order_solution):
        #             final_solutions.append(solution)
        #             break
        return final_solutions