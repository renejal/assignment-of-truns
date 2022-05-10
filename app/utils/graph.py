# libraries
import imp
from typing import List
import pandas as pd
import matplotlib.pyplot as plt
from pandas.plotting import parallel_coordinates
# import plotly.express as px

from dominio.Solution import Solution
from utils.normalize import Normalize

class Graph:

    def __init__(self, data: List[List[Solution]]) -> None:   
        dataG = []

        for index,evolution in enumerate(data):
            solutionsNormalized:List[Solution] = Normalize().normalizeFitness(evolution)
            for solution in solutionsNormalized:
                dataG.append([solution[0],solution[1],solution[2],solution[3],index+1])

        # Make the plot
        columas = ["missingShifts","assignedVigilants","extraHours","distance","Evolution"]
        dataG = pd.DataFrame(dataG,columns=columas)
        parallel_coordinates(dataG, 'Evolution', colormap=plt.get_cmap("tab20"))
        # parallel_coordinates(data, 'Iter', colormap=plt.get_cmap("Set1"))
        plt.show()
