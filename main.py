import numpy.lib.format

from VigilantAssigment import *
from File import *
from Vigilant import *
from Solution import *
from Metaheuristics.GRASP import *
import pandas as pd
import random

def bubbleSort(array):
    for iteration in range(0,len(array)-1):
        swapped =False
        for pos in range(0,len(array)-1-iteration):
            if(array[pos + 1][1] < array[pos][1]):
                aux = array[pos]
                array[pos] = array[pos+1]
                array[pos + 1] = aux
                swapped = True
        if swapped == False:
            break
    return array
def makeRCL(solutions,tam):
    solutions = bubbleSort(solutions)
    listaReducida = []
    if len(solutions) >= tam:
        listaReducida = solutions[:tam]
    else:
        listaReducida = solutions
    for element in listaReducida:
        print(element[1])




dataSet = File("Data/userInterface.csv", 4)
dataSet.procedureData()
problem = VigilantAssigment(dataSet.DataProblem, 4)
problem.to_print()
#algorithm  = Grasp()
#algorithm.Execute(problem,random.random())

"""
solutions = []
for i in range(0,10):
    solution = []
    for vigilant in range(0,100):
        shifts = []
        for period in range(0,168*24):
            sitio = random.randint(0,problem.getCantPlaces())
            if sitio != 0:
                problem.addVigilant(sitio-1,period,vigilant)
            shifts.append(sitio)
        solution.append(shifts)
    solutions.append([solution,problem.evalute(solution)])
makeRCL(solutions,9)

#listaReducida
#Continuar con el anteproyecto
#Crear el algoritmo
#Generar el csv de la solucion
"""