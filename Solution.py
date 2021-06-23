from Site import Site
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
        siteId = self.Problem.orderSitesForCantVigilantes[0]
        canNewComponents = 1
        components = []
        shifts = self.obtainWokingDay(self.Problem.getSite(siteId)) #retorna listado de jornadas para el sitio N
        for component in range(0,canNewComponents):
            site = Site(siteId)
            self.getSchedule(site,shifts)
            components.append(site)
        return component


    def getSchedule(self,site,shifts):
        if site in self.Problem.vigilantExpectedPlaces:
            vigilantsDefault = self.Problem.vigilantExpectedPlaces[site]
            for shift in shifts:
                vigilantsByPeriod = self.Problem.cantVigilantsPeriod.copy()
                cantVigilantFaltantes = vigilantsByPeriod[site][shift[0]]
                for iteration in range(0,cantVigilantFaltantes):
                    self.chooseVigilant(vigilantsDefault,site,shift)
            #si hay
        else:
            self.orderVigilantsBySite(listSiteOrderId[0], self.Problem.Vigilantes)

        return 1

    def CompleteSolution(self):
        # Haber recorrido todos los sitios
        #Aun hay sitios en la lista?
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

    def BestComponents(seslf,components):
        return components[0]
    def Union(self, component):
        #CLASE SITIO
        #Solution
        #Schedule = V[]P[]
        #Lista de VIGILANTES 
        # implementation
        return 0

   
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


