from ast import List
import random
import numpy
from utils.print_xls import generate_parameter_optimizacion
from views.general_shift_view import GenerateShiftView
from dominio.Metaheuristics.GA import *
import json
from conf.settings import SEEDS


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
    
    def __init__(self, algorithm: str, filesData: List[str]) -> None:
        self.calculate_best_parameters(algorithm, filesData)
        

    def calculate_best_parameters(self, algorithm: str, filesData: List[object]):
        random.seed(SEEDS[0])   
        views = []
        for file in filesData:
            name = file.get("name")
            time = file.get("time")
            data = open('./dataset/datasets/optimizaciones/'+ name)
            data = json.load(data)
            views.append(GenerateShiftView(data, time))
        if algorithm == 'GRASP':
            self.generate_grasp_optimization(views)
        else:
            self.generate_nsgaII_optimization(views)


    def generate_grasp_optimization(self, views: List[GenerateShiftView]):
        amount_grasp_weights = self.GRASP_INPUTS
        new_grasp_population = self.get_grasp_population()
        data = execute_ga(new_grasp_population , views, self.GRASP_ALGORITHM , amount_grasp_weights , self.sol_per_pop , self.num_generations, self.num_parents_mating)
        colums = ["evolution","solution","components_amount","restricted_list_size","tweak_amount_repetitions","amount_population","time", "average_hv"]
        data_fitness = data[0]
        data_solutions = data[1]
        generate_parameter_optimizacion(data_fitness, data_solutions, colums, self.GRASP_ALGORITHM)
    
    def generate_nsgaII_optimization(self, views: List[GenerateShiftView]):
        amount_nsgaII_weights = self.NSGAII_INPUTS
        new_nsgaII_population = self.get_nsgaII_population()
        data = execute_ga(new_nsgaII_population , views, self.NSGAII_ALGORITHM , amount_nsgaII_weights , self.sol_per_pop , self.num_generations, self.num_parents_mating)
        colums = ["evolution","solution","children_amount_to_generate","amount_parents_of_ordered_population","tweak_amount_repetitions","amount_population","time","average_hv"]
        data_fitness = data[0]
        data_solutions = data[1]
        print("-------------antes de guradar")
        generate_parameter_optimizacion(data_fitness, data_solutions, colums, self.NSGAII_ALGORITHM)


    def get_grasp_population(self):
        new_population = []
        for i in range(0, self.sol_per_pop):
            components_amount = random.randrange(10, 100, 10)
            restricted_list = random.randrange(2, 21, 2)
            if(restricted_list >= components_amount):
                restricted_list = components_amount - 5
            tweak_amount_repetitions = random.randrange(10, 51, 5)
            amount_population =  random.randrange(5, 31, 5)
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
