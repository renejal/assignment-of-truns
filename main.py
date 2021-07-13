
from Solution import *
from Metaheuristics.GRASP import Grasp
import random
random.seed(0)

listAlgoritm = [Grasp()]
myProblem = VigilantAssigment("Data/userInterface.csv","Data/vigilants.csv", 1)
for algoritm in listAlgoritm:
    algoritm.Execute(myProblem, 0)
myProblem.to_Save("Data/dataset6esult.csv")
