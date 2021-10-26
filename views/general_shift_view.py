from dominio.Metaheuristics.GRASP import Grasp
from dominio.vigilant_assigment import VigilantAssigment
import time
class GenerateShiftView:

    __algoritmGrasp = Grasp()
    __algoritmNSGA = None
    __myProblem = VigilantAssigment("dataset/userInterface.csv", "dataset/vigilants.csv", 4)

    def getShiftViglants(self):
        print("Start")
        tic = time.perf_counter()
        self.__algoritmGrasp.Execute(self.__myProblem,0,1)
        toc = time.perf_counter()
        print(f"Time {toc - tic:0.4f} seconds")



