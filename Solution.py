from Component import Component
from Site import Site
from random import random
import numpy as np
import random
from Algorithm import Algorithm
from VigilantAssigment import VigilantAssigment

class Solution:

    sitesSchedule = []
    schedule = []
    Fitness = int
    MyContainer = Algorithm
    Problem = VigilantAssigment
    

    def __init__(self, theOwner, Aletory):
        self.MyContainer = theOwner
        self.MyContainer.Aleatory = Aletory
        self.Problem = self.MyContainer.VigilantAssigment
        self.schedule = [None]*(len(self.Problem.vigilantes))
        self.sitesSchedule = [None]*(self.Problem.totalPlaces)


    def Tweak(self, Problem):

        # implementation
        return 0
    def ObtainComponents(self):
        siteId = self.Problem.orderSitesForCantVigilantes[0]
        canNewComponents = 3
        components = []
        shifts = self.obtainWokingDay(self.Problem.getSite(siteId)) #retorna listado de jornadas para el sitio N
        vigilantsByPeriod = self.Problem.cantVigilantsPeriod[siteId-1].copy()
        for component in range(0,canNewComponents):
            component = Component(self.schedule,siteId,self.Problem.totalWeeks,vigilantsByPeriod)
            site = Site(siteId)
            self.getSchedule(site,shifts)
            component.calcuteFitness()
            components.append(component)
        return components


    def getSchedule(self,site,shifts):
        vigilantsByPeriod = self.Problem.cantVigilantsPeriod.copy()
        if site in self.Problem.vigilantExpectedPlaces:
            vigilantsDefault = self.Problem.vigilantExpectedPlaces[site]
            for shift in shifts:
                cantVigilantFaltantes = vigilantsByPeriod[site][shift[0]]
                for iteration in range(0,cantVigilantFaltantes):
                    self.chooseVigilant(vigilantsDefault,site,shift)
            #si hay
        else:
            #self.orderVigilantsBySite(listSiteOrderId[0], self.Problem.Vigilantes)
            pass
        return 1

    def CompleteSolution(self):
        return True if self.sitesSchedule[len(self.sitesSchedule)-1] == None else False

    def obtainWokingDay(self,parSite):
        site = np.copy(parSite)
        working_day = []
        init = -1
        end = 0
        start = False
        k = 0
        for index, t in enumerate(site):

            if t == 0 and start == False:
                continue

            if t != 0:
                if init == -1:
                    #lleva el control cuando inicia la jornada
                    init = index
                start = True #comienza el conteo
                if k<24:
                    k +=1

            if (t==0 and start == True) or k == 24:
                workindaytimes = self.Problem.workingDay[k] # obtiene el numero de jornadas en relacion a la cantidad de horas a trabajar
                #termina el conteo
                start = False
                #se crear las jornadas a partidir de workindytimes
                working_day = working_day + (self.calculateworkinday(workindaytimes,init,index))
                #se asigna el final del turno a la variable end
                init = index+1
                #se reinicia los identificadores init y end
                k = 0


        return working_day
    def calculateworkinday(self, workinday, indexWorkingDay, endWorkingDay):
        listWorkinDay = []
        flag = False
        i = 0
        k = 0
        init = indexWorkingDay
        while indexWorkingDay <= endWorkingDay:

            if k < workinday[i]-1:
                k+=1
                indexWorkingDay+=1
            else:
                listWorkinDay.append([init,indexWorkingDay])
                indexWorkingDay +=1
                init = indexWorkingDay
                i+= 1
                k = 0
        return  listWorkinDay
    def chooseVigilant(self, vigilants,site,shift):
        vigilantID = vigilants[random.randint(0, len(vigilants)-1)]
        vigilant = self.Problem.getVigilant(vigilantID)
        if vigilant.isVigilantAvailable(shift[0],shift[1]):
            #validar guardia
            self.assigmentVigilantes(vigilant,site,shift[0],shift[1])
            return
   
    


    def assigmentVigilantes(self, objvigilant, siteId ,initShift, endShift):
        '''

        :param objvigilant: object vigilante
        :param siteId: id the site
        :param initShift: turn init for vigilant in site
        :param endShift: turn init for vigilant in site
        :return: True: assigned corretly , false if error in assigment
        '''
        if endShift > len(objvigilant.shifts):
            print("turno fuera de limite")
        for i in range(initShift,endShift):
            objvigilant.setShift(i,siteId)

    def BestComponents(self,components):   
        cantRestrictedComponets = 2
        #Fitness de la solucion
        for iteration in range(0,cantRestrictedComponets):
            swapped =False
            for pos in range(0,len(components)-1-iteration):
                if(components[pos + 1].fitness < components[pos].fitness):
                    aux = components[pos]
                    components[pos] = components[pos+1]
                    components[pos + 1] = aux
                    swapped = True
            if swapped == False:
                break
            #self.evaluteComponent()
            pass
        restrictedList = components[:5]
        return restrictedList[random.randint(0,cantRestrictedComponets-1)]
    
    def Union(self, component):
        for vigilant in component.newVigilants:
            self.schedule[vigilant.id-1] = vigilant
        self.sitesSchedule[component.siteId-1] = component.siteSchedule
   
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


