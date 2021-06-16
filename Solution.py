from Algorithm import Algorithm
from VigilantAssigment import VigilantAssigment
import operator
class Solution:

    schedule = []
    Fitness = int

   # MyContainer = Algorithm
    

    def __init__(self, theOwner):
        self.MyContainer = theOwner
        solution = []


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
    def obtainFirsWokingDay(self,site):
        start = False
        stop = False
        workinDay = []
        k = 0
        for index, t in enumerate(site):
            if t == 1:
                start = True
                if k<24:
                    workinDay.append(t)
                    k = +1
                else:
                    stop = True

            elif start == True or stop == True:
                pass










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
    def orderVigilantsBySite(self,place,vigilants):
        for iteration in range(0,len(vigilants)-1):
            swapped =False
            for pos in range(0,len(vigilants)-1-iteration):
                if(vigilants[pos + 1].distances[place-1] < vigilants[pos].distances[place-1]):
                    aux = vigilants[pos]
                    vigilants[pos] = vigilants[pos+1]
                    vigilants[pos + 1] = aux
                    swapped = True
            if swapped == False:
                break
        return vigilants 


