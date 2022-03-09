# libraries
import pandas as pd
import matplotlib.pyplot as plt
from pandas.plotting import parallel_coordinates

class Graph:

    def __init__(self, data) -> None:   
        # Make the plot
        columas = ["missingShifts","assignedVigilants","extraHours","distance","Solution","Iter"]
        data = pd.DataFrame(data,columns=columas)
        parallel_coordinates(data, 'Solution', colormap=plt.get_cmap("spring"))
        # parallel_coordinates(data, 'Iter', colormap=plt.get_cmap("Set1"))
        plt.show()

