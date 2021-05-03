from VigilantAssigment import *
from fileProblem import *
import pandas as pd
import random


dataSet = FileProblem("Data/userInterface.csv",4)
dataSet.procedureData()
problem = VigilantAssigment(dataSet.DataProblem,4)  
solution = []
for vigilant in range(0,100):
    shifts = []
    for period in range(0,168*4):
        sitio = random.randint(0,problem.getCantPlaces())
        if sitio != 0:
            problem.addVigilant(sitio-1,period,vigilant)
        shifts.append(sitio)
    solution.append(shifts)
problem.evalute(solution)

#Continuar con el anteproyecto
#Crear el algoritmo
#Generar el csv de la solucion
