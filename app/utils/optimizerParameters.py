import random
import numpy
from utils.print_xls import generate_parameter_optimizacion
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
    sol_per_pop = 10
    num_parents_mating = 2
    num_generations = 3

    def __init__(self) -> None:
        pass

    def calculate_best_parameters(self, view: GenerateShiftView):
        # self.generate_grasp_optimization(view)
        self.generate_nsgaII_optimization(view)


    def generate_grasp_optimization(self,view: GenerateShiftView):
        amount_grasp_weights = self.GRASP_INPUTS
        new_grasp_population = self.get_grasp_population()
        data = execute_ga(new_grasp_population , view, self.GRASP_ALGORITHM , amount_grasp_weights , self.sol_per_pop , self.num_generations, self.num_parents_mating)
        colums = ["evolution","solution","components_amount","restricted_list_size","tweak_amount_repetitions","amount_population","time", "average_hv"]
        generate_parameter_optimizacion(data, colums, self.GRASP_ALGORITHM)
    
    def generate_nsgaII_optimization(self,view: GenerateShiftView):
        amount_nsgaII_weights = self.NSGAII_INPUTS
        new_nsgaII_population = self.get_nsgaII_population()
        data = execute_ga(new_nsgaII_population , view, self.NSGAII_ALGORITHM , amount_nsgaII_weights , self.sol_per_pop , self.num_generations, self.num_parents_mating)
        colums = ["evolution","solution","children_amount_to_generate","amount_parents_of_ordered_population","tweak_amount_repetitions","amount_population","time","average_hv"]
        generate_parameter_optimizacion(data, colums, self.GRASP_ALGORITHM)


    def get_grasp_population(self):
        new_population = []
        for i in range(0, self.sol_per_pop):
            components_amount = random.randrange(10, 51, 10)
            restricted_list = random.randrange(2, 21, 2)
            tweak_amount_repetitions = random.randrange(10, 31, 5)
            amount_population =  random.randrange(6, 13, 2)
            new_population.append([components_amount, restricted_list, tweak_amount_repetitions, amount_population])
        return numpy.array(new_population)
    
    def get_nsgaII_population(self):
        new_population = []
        for i in range(0, self.sol_per_pop):
            children_amount_to_generate = random.randrange(2, 10, 1)
            NUM_PARENTS_OF_ORDERED_POPULATION = random.uniform(0, 1)
            NUMBER_ITERATION_SELECTION_COMPONENTE = random.randrange(5,15,1)
            amount_population =  random.randrange(10, 20, 2)
            new_population.append([children_amount_to_generate, NUM_PARENTS_OF_ORDERED_POPULATION, NUMBER_ITERATION_SELECTION_COMPONENTE, amount_population])
        return numpy.array(new_population)
