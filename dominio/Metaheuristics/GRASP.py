import random

from dominio.Algorithm import Algorithm
from dominio.Solution import Solution
from dominio.vigilant_assigment import VigilantAssigment
import copy

class Grasp(Algorithm):
    CurrentEFOs: int = 0
    MaxEFOs: int = 10

    def Execute(self, problem: VigilantAssigment, Aleatory, numComponets):
        random.seed(Aleatory)
        Best = None
        while self.CurrentEFOs < self.MaxEFOs:
            S = Solution(problem, Aleatory)
            i  = 1
            while S.is_solution_complete():
                components = S.create_components(numComponets)
                RestrictedList = components
                print("iteration:"+ str(i))
                i+=1
                if RestrictedList == None:
                    continue
                else:
                    BestRestrictedList = S.get_best_components(RestrictedList,1)
                    S.merge_component(BestRestrictedList)
            for m in range(0,3):
                print("TWEAKK:"+str(m))
                newSolution = self.Tweak(copy.copy(S))
                if newSolution.Fitness < S.__fitness:
                    S = newSolution
            if Best == None or S.__fitness < Best.__fitness:
                Best = S
            self.CurrentEFOs+=1
            print("Nueva  iteracion")
        return Best

    def Tweak(self,solution):
        return solution.Tweak(solution)








