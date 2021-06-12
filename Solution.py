from Algorithm import Algorithm
from VigilantAssigment import VigilantAssigment
import operator
class Solution:

    schedule = []
    Fitness = int
   # MyContainer = Algorithm
    

    #def __init__(self, theOwner):
     #   self.MyContainer = theOwner
      #  solution = []


    def Tweak(self, Problem):

        # implementation
        return 0

    def ObtainComponents(self, problem):
        listSiteOrderId = self.OrderSitesForCantVigilantes(self, problem)
        print("sitios ordenados por cantidad de vigilantes:",listSiteOrderId)
        return 0

    def CompleteSolution(self):
        # implementation
        return 0

    def Union(self, components):
        # implementation
        return 0

    def OrderSitesForCantVigilantes(self, problem):
        sites = problem.vigilantesforSite
        sites = sorted(sites.items(), key=operator.itemgetter(1), reverse=True)
        site = []
        for i in sites:
            site.append(i[0])
        return site



