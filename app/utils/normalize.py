from typing import List
from dominio.Solution import Solution

class Normalize:

    missing_shifts_fitnessMax: int = 10
    assigned_vigilantes_fitnessMax:int =  10
    extra_hours_fitnessMax:int = 20
    distance_fitnessMax:int = 100
    missing_shifts_fitnessMin: int = 0
    assigned_vigilantes_fitnessMin:int =  0
    extra_hours_fitnessMin:int = 0
    distance_fitnessMin:int = 0

    def normalizeFitness(self, solutions: List[Solution]) -> List[Solution]:
        fitnessMax = [self.missing_shifts_fitnessMax, self.assigned_vigilantes_fitnessMax, self.extra_hours_fitnessMax, self.distance_fitnessMax]
        fitnessMin = [self.missing_shifts_fitnessMin, self.assigned_vigilantes_fitnessMin, self.extra_hours_fitnessMin, self.distance_fitnessMin]
        solutionsNormalizated: List[List[int]] = []

        #Eliminar este for y calcular el verdadero maximoFitness para cada objetivo
        for solution in solutions:
            self.getMaxFitnessSolution(solution,fitnessMax)

        for solution in solutions:
            missing_shifts_fitness = self.normalize(
                solution.missing_shifts_fitness, fitnessMax[0], fitnessMin[0])
            assigned_vigilantes_fitness = self.normalize(
                solution.assigned_vigilantes_fitness, fitnessMax[1], fitnessMin[1])
            extra_hours_fitness = self.normalize(
                solution.extra_hours_fitness, fitnessMax[2], fitnessMin[2])
            distance_fitness = self.normalize(
                solution.distance_fitness, fitnessMax[3], fitnessMin[3])
            solutionsNormalizated.append([missing_shifts_fitness, assigned_vigilantes_fitness,
                         extra_hours_fitness, distance_fitness])
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
