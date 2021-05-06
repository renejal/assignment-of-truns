from Algorithm import Algorithm
from Solution import Solution
import copy

class Grasp(Algorithm):
    CurrentEFOs = 0
    MaxEFOs = 10000

    def Execute(self, Problem, Aleatory):
        Best:Solution
        while self.CurrentEFOs < self.MaxEFOs:
            S = Solution(Problem, Aleatory)

            while S.CompleteSolution():
                RestrictedList = S.ObtainComponents()
                if RestrictedList:
                    S = Solution(Problem, Aleatory)
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













