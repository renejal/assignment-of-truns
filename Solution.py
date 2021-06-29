from Component import Component
from Site import Site
from random import random
import numpy as np
import random
import Vigilant

random.seed(0)
from Algorithm import Algorithm
from VigilantAssigment import VigilantAssigment

class Solution:

    sitesSchedule = []
    schedule = []
    Fitness = int
    MyContainer = Algorithm
    Problem = VigilantAssigment
    vigilantsForPlaces = None
    

    def __init__(self, theOwner, Aletory):
        self.MyContainer = theOwner
        self.MyContainer.Aleatory = Aletory
        self.Problem = self.MyContainer.VigilantAssigment

        self.vigilantsForPlaces = []
        self.initVigilsForPlaces()
        solution = []
    def initVigilsForPlaces(self):
        for i in range(0,self.Problem.totalPlaces):
            self.vigilantsForPlaces.append([])

        self.schedule = [None]*(len(self.Problem.vigilantes))
        self.sitesSchedule = [None]*(self.Problem.totalPlaces)



    def Tweak(self, Problem):

        # implementation
        return 0
    def ObtainComponents(self):
        listSiteOrderId = self.OrderSitesForCantVigilantes(self.Problem)
        if listSiteOrderId[0] in self.Problem.vigilantExpectedPlaces:

            workingDayList = self.obtainWokingDay(self.Problem.getSite(listSiteOrderId[0]))
            for shift in workingDayList:
                vigilantsByPeriod = self.Problem.cantVigilantsPeriod.copy()
                cantVigilantFaltantes = vigilantsByPeriod[listSiteOrderId[0]][shift[0]]
                for iteration in range(0,cantVigilantFaltantes):
                    # todo: Calcular guardia necesarios para el sitio
                    self.chooseVigilant(listSiteOrderId[0],shift)
            #si hay
        else:
            self.orderVigilantsBySite(listSiteOrderId[listSiteOrderId[0]], self.Problem.Vigilantes)

        siteId = self.Problem.orderSitesForCantVigilantes[0]
        canNewComponents = 3
        components = []
        shifts = self.obtainWokingDay(self.Problem.getSite(siteId)) #retorna listado de jornadas para el sitio N
        vigilantsByPeriod = self.Problem.cantVigilantsPeriod[siteId-1].copy()
        necesaryVigilantes - self.getNecessaryVigilants(vigilantsByPeriod)
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
        # implementation
        return 1
    def aleatory(self,init, end):
        return random.randint(init, end)
    def assignVigilantsmissingofSite(self, siteId):
        workingday = self.Problem.workingDay(siteId)


    def obtainVigilantAvailable(self,site, InitShift, endShift):
        varResultado = None
        #1 vigilante de los asignados al sitio
        for i in range(0,10):
            #todo : revisar el limite superios del for, cuentas iteraciones se podrian hacer en caso de que no encuentr un vigilantes valido??
            vigilantDefaulList =self.Problem.vigilantExpectedPlaces[site]
            vigilantId = self.aleatory(0,len(vigilantDefaulList))
            objVigilant = self.Problem.getVigilant(vigilantId)
            if objVigilant.isVigilantAvailable(InitShift,endShift):
                varResultado = objVigilant

        #2 si no existe vigilante valido dentro del sitio se toma uno de la lista de vigilantes global y se asigna a la lista de vigi
        #lantes para el sitio
        for i in range(0,len(self.Problem.totalVigilantes)):
            vigilantId = self.aleatory(0, len(self.Problem.vigilantExpectedPlaces(site)))
            objVigilant = self.Problem.getVigilant(vigilantId)
            if objVigilant.isVigilantAvailable(InitShift,endShift):
                varResultado = objVigilant


        return varResultado
       # return True if self.sitesSchedule[len(self.sitesSchedule)-1] == None else False

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
    def chooseVigilant(self,site,shift):
        '''
        assigns vigilants to the shift
        :param vigilantsDefault:
        :param site:
        :param shift:
        :return:
        '''
        objVigilant = self.obtainVigilantAvailable(site, shift[0],shift[1])#todo: escoger vigilantes por preferencias y agregar vigilantes faltantes a la lista
        if objVigilant != None:
            if objVigilant.isVigilantAvailable(shift[0],shift[1]):
                #validar guardia
                if self.assigmentVigilantes(objVigilant, site, shift[0],shift[1]):
                    self.vigilantsForPlaces[site-1].append(objVigilant.id)

        else:
            pass
            #empty list



    


    def assigmentVigilantes(self, objvigilant, siteId ,initShift, endShift):
        '''
        :param objvigilant: object vigilante
        :param siteId: id the site
        :param initShift: turn init for vigilant in site
        :param endShift: turn init for vigilant in site
        :return: True: assigned corretly , false if error in assigment
        '''
        varResult = False
        for i in range(initShift, endShift):
            objvigilant.setShift(i, siteId)
            varResult = True
        return varResult

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

    def getNecessaryVigilants(self,vigilantsByPeriod):
        vigilantsByPeriodInAWeek = vigilantsByPeriod[:168]
        
