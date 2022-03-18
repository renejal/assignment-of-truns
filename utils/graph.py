# libraries
from typing import List
import pandas as pd
import matplotlib.pyplot as plt
from pandas.plotting import parallel_coordinates
# import plotly.express as px

from dominio.Solution import Solution

class Graph:

    def __init__(self, data: List[List[Solution]]) -> None:   
        dataG = []
        fitnessMax = [0,0,0,0]
        fitnessMin = [0,0,0,0]

        for index,evolution in enumerate(data):
            for solution in evolution:
                self.getMaxFitnessSolution(solution,fitnessMax)
                # self.getMinFitnessSolution(solution,fitnessMin)
        for index,evolution in enumerate(data):
            for solution in evolution:
                missing_shifts_fitness = self.normalize(solution.missing_shifts_fitness,fitnessMax[0],fitnessMin[0])
                assigned_vigilantes_fitness = self.normalize(solution.assigned_vigilantes_fitness,fitnessMax[1],fitnessMin[1])
                extra_hours_fitness = self.normalize(solution.extra_hours_fitness,fitnessMax[2],fitnessMin[2])
                distance_fitness = self.normalize(solution.distance_fitness,fitnessMax[3],fitnessMin[3])
                dataG.append([missing_shifts_fitness,assigned_vigilantes_fitness,extra_hours_fitness,distance_fitness,index+1])

        # Make the plot
        columas = ["missingShifts","assignedVigilants","extraHours","distance","Evolution"]
        dataG = pd.DataFrame(dataG,columns=columas)
        parallel_coordinates(dataG, 'Evolution', colormap=plt.get_cmap("tab20"))
        # parallel_coordinates(data, 'Iter', colormap=plt.get_cmap("Set1"))
        plt.show()

    def normalize(self,valor, maximo, minimo):
        if maximo == 0:
            return 0
        return (valor-minimo)/(maximo-minimo)

    def getMaxFitnessSolution(self, solution:Solution, fitnessMax: List[int]):
        if solution.missing_shifts_fitness > fitnessMax[0]:
                    fitnessMax[0] = solution.missing_shifts_fitness
        if solution.assigned_vigilantes_fitness > fitnessMax[1]:
            fitnessMax[1] = solution.assigned_vigilantes_fitness
        if solution.extra_hours_fitness > fitnessMax[2]:
            fitnessMax[2] = solution.extra_hours_fitness
        if solution.distance_fitness > fitnessMax[3]:
            fitnessMax[3] = solution.distance_fitness
    
    def getMinFitnessSolution(self, solution:Solution, fitnessMin: List[int]):
        if solution.missing_shifts_fitness < fitnessMin[0]:
            fitnessMin[0] = solution.missing_shifts_fitness
        if solution.assigned_vigilantes_fitness < fitnessMin[1]:
            fitnessMin[1] = solution.assigned_vigilantes_fitness
        if solution.extra_hours_fitness < fitnessMin[2]:
            fitnessMin[2] = solution.extra_hours_fitness
        if solution.distance_fitness < fitnessMin[3]:
            fitnessMin[3] = solution.distance_fitness