import random
import numpy
from views.general_shift_view import GenerateShiftView
from dominio.Metaheuristics.GA import *


class OptimizerParamets:
    # Inputs of the equation.
    GRASP_ALGORITHM = "GRASP"
    GRASP_INPUTS = 3
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
        num_weights = self.GRASP_INPUTS
        # Creating the initial population.
        new_population = self.get_grasp_population()
        execute_ga(new_population , view, self.GRASP_ALGORITHM , num_weights , self.sol_per_pop , self.num_generations, self.num_parents_mating)

    def get_grasp_population(self):
        new_population = []
        for i in range(0, self.sol_per_pop):
            components_amount = random.randrange(10, 100, 10)
            restricted_list = random.randrange(3, components_amount*0.3, 2)
            tweak_amount_repetitions = random.randrange(10, 100, 10)
            # amount_poblation Agregar?
            new_population.append([components_amount, restricted_list, tweak_amount_repetitions])
        return numpy.array(new_population)
