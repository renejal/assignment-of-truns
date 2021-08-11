import random

from Algorithm import Algorithm
from Solution import Solution
import copy

class Grasp(Algorithm):
    CurrentEFOs = 0
    MaxEFOs = 10

    def Execute(self, Problem, Aleatory):
        self.VigilantAssigment = Problem
        random.seed(Aleatory)
        Best = None
        while self.CurrentEFOs < self.MaxEFOs:
            S = Solution(self, Aleatory)
            while S.CompleteSolution():
                RestrictedList = S.ObtainComponents(20)
                if RestrictedList == None:
                    #S = Solution(Problem, Aleatory)
                    #Next Site
                    continue
                else:
                    BestRestrictedList = S.BestComponents(RestrictedList,5)
                    S.Union(BestRestrictedList)
            S.generateResults(0,self.MaxEFOs)
            #Comparar si la nueva solucion es mejor que la anterior
            for m in range(0,10):
                newSolution = self.Tweak(copy.copy(S))
                if newSolution.Fitness < S.Fitness:
                    S = newSolution
            if Best == None or S.Fitness < Best.Fitness:
                Best = S
            self.CurrentEFOs+=1
            print("Nueva  iteracion")
        Best.generateResults(0,self.MaxEFOs)
        return Best

    def Tweak(self,solution):
        return solution.Tweak(solution)








