from random import random
import numpy as np
import random

from Algorithm import Algorithm
from VigilantAssigment import VigilantAssigment
import operator
class Solution:

    schedule = []
    Fitness = int
    MyContainer = Algorithm
    Problem = VigilantAssigment
    

    def __init__(self, theOwner, Aletory):
        self.MyContainer = theOwner
        self.MyContainer.Aleatory = Aletory
        self.Problem = self.MyContainer.VigilantAssigment
        solution = []




    def Tweak(self, Problem):

        # implementation
        return 0

    def ObtainComponents(self):
        listSiteOrderId = self.OrderSitesForCantVigilantes(self.Problem)
        
        jornada, site=self.obtainFirsWokingDay(self.Problem.getSite(listSiteOrderId[0]))
        if (listSiteOrderId[0] in self.Problem.vigilantExpectedPlaces) == True:
            vigilantsDefault = self.Problem.vigilantExpectedPlaces[listSiteOrderId[0]]
            shift = [165,173]
            self.chooseVigilant(vigilantsDefault,shift)
            #si hay
        else:
            self.orderVigilantsBySite(listSiteOrderId[0], self.Problem.Vigilantes)

        return 1

    def CompleteSolution(self):
        # implementation
        return 1
    def obtainFirsWokingDay(self,parSite):
        site = np.copy(parSite)
        start = False
        k = 0
        for index, t in enumerate(site):

            if t == 0 and start == False:
                continue
            elif t==0 and start == True:
                break
            if t != 0:
                start = True
                if k<24:
                    site = np.delete(site,0)
                    k +=1

                else:
                    print("cumplio el limite de horas por jornada de 24 horas")
                    break

        if start == True:
            workin_day=self.Problem.workingDay[k]
            return workin_day,site

    def chooseVigilant(self, vigilants,shift):
        vigilantID = vigilants[random.randint(0, len(vigilants)-1)]
        vigilant = self.Problem.getVigilant(vigilantID)
        if vigilant.availabilityShift(shift[0],shift[1]):
            #assignVigilant(site,vigilant,shift[0],shift[1])  
            return










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


