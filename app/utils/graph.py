# libraries
import imp
from typing import List
import pandas as pd
import matplotlib.pyplot as plt
# from pandas.plotting import parallel_coordinates
import plotly.express as px

from dominio.Solution import Solution
from utils.normalize import Normalize

class Graph:

    def __init__(self, evolutions: List[List[Solution]]) -> None:   
        dataG = []
        normalize = Normalize()
        for index,evolution in enumerate(evolutions):
            solutionsNormalized:List[Solution] = normalize.normalizeFitness(evolution)
            for solution in solutionsNormalized:
                dataG.append([solution[0],solution[1],solution[2],solution[3],index+1])

        # Make the plot
        fitness_max = normalize.get_fitness_max()
        columas = ["missingShifts "+str(fitness_max[0]) ,"assignedVigilants "+str(fitness_max[1]),"extraHours "+str(fitness_max[2]),"distance "+str(fitness_max[3]),"Evolution"]
        dataG = pd.DataFrame(dataG,columns=columas)
        # parallel_coordinates(dataG, 'Evolution', colormap=plt.get_cmap("tab20"))
        # # parallel_coordinates(data, 'Iter', colormap=plt.get_cmap("Set1"))
        # plt.savefig
        # plt.show()
        self.fig = px.parallel_coordinates(dataG, color="Evolution",
                              dimensions=["missingShifts "+str(fitness_max[0]) ,"assignedVigilants "+str(fitness_max[1]),"extraHours "+str(fitness_max[2]),"distance "+str(fitness_max[3])],
                              color_continuous_scale=px.colors.sequential.Rainbow
                              )

    def get_fig(self):
        return self.fig