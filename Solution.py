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
        for site in listSiteOrderId:

            if site in self.Problem.vigilantExpectedPlaces:
                vigilantsDefault = self.Problem.vigilantExpectedPlaces[site]
                workingDayList = self.obtainWokingDay(self.Problem.getSite(site))
                for shift in workingDayList:
                    vigilantsByPeriod = self.Problem.cantVigilantsPeriod.copy()
                    cantVigilantFaltantes = vigilantsByPeriod[site][shift[0]]
                    for iteration in range(0,cantVigilantFaltantes):
                        # todo: Calcular guardia necesarios para el sitio
                        self.chooseVigilant(vigilantsDefault,site,shift)
                #si hay
            else:
                self.orderVigilantsBySite(listSiteOrderId[site], self.Problem.Vigilantes)

        return 1
    def CompleteSolution(self):
        # implementation
        return 1
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
        vigilantID = vigilants[random.randint(0, len(vigilants)-1)]#todo: escoger vigilantes por preferencias y agregar vigilantes faltantes a la lista
        vigilant = self.Problem.getVigilant(vigilantID)
        if vigilant.isVigilantAvailable(shift[0],shift[1]):
            #validar guardia
            self.assigmentVigilantes(vigilant,site,shift[0],shift[1])
   
    


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
        for i in range(initShift, endShift):
            objvigilant.setShift(i, siteId)


    def Union(self, components):
        # implementation
        return 0

    def OrderSitesForCantVigilantes(self, problem):
        sites = problem.vigilantesforSite
        sites = sorted(sites.items(), key=operator.itemgetter(1), reverse=True)
        site = []
        for i in sites:
            site.append(int(i[0]))
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


