#Minimizar la cantidad de turnos faltantes.
#Minimzar la distancia del vigilante al puesto de trabajo.
#Minimizar la cantidad de guardias a utilizar para el problema.
#Minimizar numero de horas extras trabajadas.
#--------------TO DO-----------------------
#La restricción (10) se asegura que cada personal de seguridad y vigilancia deba trabajar un mínimo de periodos a la semana

#La restricción (11) define que la duración mínima obligatoria de un turno para un sitio debe ser mayor y menor a la cantidad de horas de los turnos generales
#Qk=Duración mínima del turno que se debe vigilar en un sitio k obligatoriamente.

# Separar el fitness por funcion objetivo



import time
from Solution import *
from Metaheuristics.GRASP import Grasp

listAlgoritm = [Grasp()]
myProblem = VigilantAssigment("Data/userInterface.csv","Data/vigilants.csv", 4)
for algoritm in listAlgoritm:
    print("Start")
    tic = time.perf_counter()
    algoritm.Execute(myProblem, 0)
    toc = time.perf_counter()
    print(f"Time {toc - tic:0.4f} seconds")

#Validara como calcular el fitness