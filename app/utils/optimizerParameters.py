import random
import numpy
from views.general_shift_view import GenerateShiftView
from dominio.Metaheuristics.GA import *


class OptimizerParamets:
    # Inputs of the equation.
    GRASP_ALGORITHM = "GRASP"
    GRASP_INPUTS = 4
    NSGAII_ALGORITHM = "NSGAII"
    NSGAII_INPUTS = 4
    """
        Genetic algorithm parameters:
            Mating pool size
            Population size
    """
    sol_per_pop = 4
    num_parents_mating = 2
    num_generations = 5

    def __init__(self) -> None:
        pass

    def calculate_best_parameters(self, view: GenerateShiftView):
        # Number of the weights we are looking to optimize.
        amount_grasp_weights = self.GRASP_INPUTS
        amount_nsgaII_weights = self.NSGAII_INPUTS
        # Creating the initial population.
        new_grasp_population = self.get_grasp_population()
        execute_ga(new_grasp_population , view, self.GRASP_ALGORITHM , amount_grasp_weights , self.sol_per_pop , self.num_generations, self.num_parents_mating)
        # new_nsgaII_population = self.get_nsgaII_population()
        # execute_ga(new_nsgaII_population , view, self.NSGAII_ALGORITHM , amount_nsgaII_weights , self.sol_per_pop , self.num_generations, self.num_parents_mating)

    def get_grasp_population(self):
        new_population = []
        for i in range(0, self.sol_per_pop):
            components_amount = random.randrange(10, 100, 10)
            restricted_list = random.randrange(3, components_amount*0.3, 2)
            tweak_amount_repetitions = random.randrange(10, 100, 10)
            amount_population =  random.randrange(10, 20, 2)
            new_population.append([components_amount, restricted_list, tweak_amount_repetitions, amount_population])
        return numpy.array(new_population)
    
    def get_nsgaII_population(self):
        new_population = []
        for i in range(0, self.sol_per_pop):
            children_amount_to_generate = random.randrange(1, 2, 10)
            amount_parents_of_ordered_population = random.randrange(1, 1, 10)
            tweak_amount_repetitions = random.randrange(1, 1, 10)
            amount_population =  random.randrange(10, 20, 2)
            new_population.append([children_amount_to_generate, amount_parents_of_ordered_population, tweak_amount_repetitions, amount_population])
        return numpy.array(new_population)
