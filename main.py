
from Solution import *
from Metaheuristics.GRASP import Grasp

listAlgoritm = [Grasp()]
myProblem = VigilantAssigment("Data/userInterface.csv","Data/vigilants.csv", 4)
for algoritm in listAlgoritm:
    algoritm.Execute(myProblem, 0)
