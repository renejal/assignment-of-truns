import time
from Solution import *
from Metaheuristics.GRASP import Grasp

listAlgoritm = [Grasp()]
myProblem = VigilantAssigment("Data/userInterfaceFinal.csv","Data/vigilantsFinal.csv", 4)
for algoritm in listAlgoritm:
    print("Start")
    tic = time.perf_counter()
    algoritm.Execute(myProblem, 0)
    toc = time.perf_counter()
    print(f"Time {toc - tic:0.4f} seconds")

#Validara como calcular el fitness