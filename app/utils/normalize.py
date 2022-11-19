from copy import copy
import math
from typing import List
from dominio.Solution import Solution
from conf.settings import MISSING_FITNESS_VALUE,ASSIGNED_VIGILANTES_FITNESS_VALUE,DISTANCE_FITNESS_VALUE,EXTRA_HOURS_FITNESS_VALUE,MAXIMUM_WORKING_AMOUNT_HOURS_BY_WEEK

class Normalize:

    missing_shifts_fitness_acceptable_porcentage: float = 0
    assigned_vigilantes_acceptable_porcentage: float = 0
    extra_hours_acceptable_porcentage: float = 0
    distance_acceptable_porcentage: float = 0
    # missing_shifts_fitness_acceptable_porcentage: float = 0.95
    # assigned_vigilantes_acceptable_porcentage: float = 0.2
    # extra_hours_acceptable_porcentage: float = 0.2
    # distance_acceptable_porcentage: float = 0.1
    fitnessMax: List[int]

    def normalizeFitness(self, population: List[Solution]) -> List[List[int]]:
        fitnessMax = copy(population[0].problem.max_possible_fitness) 
        fitnessMin = [0,0,0,0]
        fitnessMax[0] = math.ceil(fitnessMax[0]*(1-self.missing_shifts_fitness_acceptable_porcentage))
        fitnessMax[1] = math.ceil(fitnessMax[1]*(1-self.assigned_vigilantes_acceptable_porcentage))
        fitnessMax[2] = math.ceil(fitnessMax[2]*(1-self.extra_hours_acceptable_porcentage))
        fitnessMax[3] = math.ceil(fitnessMax[3]*(1-self.distance_acceptable_porcentage))
        solutionsNormalizated: List[List[int]] = []
        suma =0
        for solution in population:
            suma += solution.total_fitness
            missing_shifts_fitness = self.normalize(solution.missing_shifts_fitness / MISSING_FITNESS_VALUE, fitnessMax[0], fitnessMin[0])
            # solution.assigned_vigilantes_fitness = solution.calculate_assigned_vigilantes_fitness()
            assigned_vigilantes_fitness = self.normalize(solution.assigned_vigilantes_fitness / MAXIMUM_WORKING_AMOUNT_HOURS_BY_WEEK /2, fitnessMax[1], fitnessMin[1])
            # assigned_vigilantes_fitness = self.normalize(solution.assigned_vigilantes_fitness, fitnessMax[1], fitnessMin[1])
            extra_hours_fitness = self.normalize(solution.extra_hours_fitness / EXTRA_HOURS_FITNESS_VALUE, fitnessMax[2], fitnessMin[2])
            distance_fitness = self.normalize(solution.distance_fitness / DISTANCE_FITNESS_VALUE, fitnessMax[3], fitnessMin[3])
            solutionsNormalizated.append([missing_shifts_fitness, assigned_vigilantes_fitness,
                                          extra_hours_fitness, distance_fitness])
        self.fitnessMax = fitnessMax
        return solutionsNormalizated

    def normalize(self, valor, maximo, minimo):
        if maximo == 0:
            return 0
        return (valor-minimo)/(maximo-minimo)

    def getMaxFitnessSolution(self, solution: Solution, fitnessMax: List[int]):
        if solution.missing_shifts_fitness > fitnessMax[0]:
            fitnessMax[0] = solution.missing_shifts_fitness
        if solution.assigned_vigilantes_fitness > fitnessMax[1]:
            fitnessMax[1] = solution.assigned_vigilantes_fitness
        if solution.extra_hours_fitness > fitnessMax[2]:
            fitnessMax[2] = solution.extra_hours_fitness
        if solution.distance_fitness > fitnessMax[3]:
            fitnessMax[3] = solution.distance_fitness

    def getMinFitnessSolution(self, solution: Solution, fitnessMin: List[int]):
        if solution.missing_shifts_fitness < fitnessMin[0]:
            fitnessMin[0] = solution.missing_shifts_fitness
        if solution.assigned_vigilantes_fitness < fitnessMin[1]:
            fitnessMin[1] = solution.assigned_vigilantes_fitness
        if solution.extra_hours_fitness < fitnessMin[2]:
            fitnessMin[2] = solution.extra_hours_fitness
        if solution.distance_fitness < fitnessMin[3]:
            fitnessMin[3] = solution.distance_fitness

    def get_fitness_max(self):
        return self.fitnessMax

    def normalizeGraph(self, population: List[Solution]) -> List[List[int]]:
        fitnessMax = copy(population[0].problem.max_possible_fitness) 
        fitnessMax[1] = population[0].problem.total_vigilantes
        fitnessMin = [0,0,0,0]
        fitnessMax[0] = math.ceil(fitnessMax[0]*(1-self.missing_shifts_fitness_acceptable_porcentage))
        fitnessMax[1] = math.ceil(fitnessMax[1]*(1-self.assigned_vigilantes_acceptable_porcentage))
        fitnessMax[2] = math.ceil(fitnessMax[2]*(1-self.extra_hours_acceptable_porcentage))
        fitnessMax[3] = math.ceil(fitnessMax[3]*(1-self.distance_acceptable_porcentage))
        solutionsNormalizated: List[List[int]] = []
        suma =0
        for solution in population:
            suma += solution.total_fitness
            missing_shifts_fitness = self.normalize(solution.missing_shifts_fitness / MISSING_FITNESS_VALUE, fitnessMax[0], fitnessMin[0])
            fitnessvigilant = solution.calculate_assigned_vigilantes_fitness()
            assigned_vigilantes_fitness = self.normalize(fitnessvigilant, fitnessMax[1], fitnessMin[1])
            # assigned_vigilantes_fitness = self.normalize(solution.assigned_vigilantes_fitness, fitnessMax[1], fitnessMin[1])
            extra_hours_fitness = self.normalize(solution.extra_hours_fitness / EXTRA_HOURS_FITNESS_VALUE, fitnessMax[2], fitnessMin[2])
            distance_fitness = self.normalize(solution.distance_fitness / DISTANCE_FITNESS_VALUE, fitnessMax[3], fitnessMin[3])
            solutionsNormalizated.append([missing_shifts_fitness, assigned_vigilantes_fitness,
                                          extra_hours_fitness, distance_fitness])
        self.fitnessMax = fitnessMax
        return solutionsNormalizated
