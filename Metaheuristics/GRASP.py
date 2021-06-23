from Algorithm import Algorithm
from Solution import Solution
import copy

class Grasp(Algorithm):
    CurrentEFOs = 0
    MaxEFOs = 10000

    def Execute(self, Problem, Aleatory):
        self.VigilantAssigment = Problem;
        self.Aleatory = Aleatory;
        Best:Solution
        while self.CurrentEFOs < self.MaxEFOs:
            S = Solution(self, Aleatory)

            while S.CompleteSolution():
                
                RestrictedList = S.ObtainComponents()
                if RestrictedList == None:
                    #S = Solution(Problem, Aleatory)
                    #Next Site
                    continue
                else:
                    BestRestrictedList = S.BestComponents()
                    S = S.Union(BestRestrictedList)

        for m in self.LengthTime:

            R:Solution = self.Tweak(copy.copy(self.S))
            if R.Fitness > S.Fitness:
                S = R
            if Best or S.Fitness > Best.Fitness:
                Best = S

        return Best













