from Algorithm import Algorithm
from Solution import Solution
import copy

class Grasp(Algorithm):
    CurrentEFOs = 0
    MaxEFOs = 10

    def Execute(self, Problem, Aleatory):
        self.VigilantAssigment = Problem;
        self.Aleatory = Aleatory;
        Best:Solution
        while self.CurrentEFOs < self.MaxEFOs:
            S = Solution(self, Aleatory)
            while S.CompleteSolution():
                RestrictedList = S.ObtainComponents(10)
                if RestrictedList == None:
                    #S = Solution(Problem, Aleatory)
                    #Next Site
                    continue
                else:
                    BestRestrictedList = S.BestComponents(RestrictedList,3)
                    S.Union(BestRestrictedList)
            #Comparar si la nueva solucion es mejor que la anterior
            S.generateResults(self.CurrentEFOs,self.MaxEFOs)
            self.CurrentEFOs+=1
        for m in range(0,10):

            R:Solution = self.Tweak(copy.copy(self.S))
            if R.Fitness > S.Fitness:
                S = R
            if Best or S.Fitness > Best.Fitness:
                Best = S

        return Best













