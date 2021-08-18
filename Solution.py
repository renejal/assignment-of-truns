from typing import overload
from Vigilant import Vigilant
from Component import Component
from random import choice, random
import random
import math
import numpy as np
from Algorithm import Algorithm
from VigilantAssigment import VigilantAssigment
import copy 
import collections

class Solution:

    sitesSchedule = []
    vigilantsSchedule = []
    Fitness = 0
    MyContainer = Algorithm
    Problem = VigilantAssigment
    missingShiftsBySite = []
    Aleatory = None

    def __init__(self, theOwner, Aletory):
        random.seed(Aletory)
        self.MyContainer = theOwner
        self.MyContainer.Aleatory = Aletory
        self.Problem = self.MyContainer.VigilantAssigment
        self.vigilants = self.Problem.vigilantes.copy()

        self.sitesSchedule = [[]]*(self.Problem.totalPlaces)
        self.vigilantsSchedule = self.Problem.vigilantes.copy()
        self.missingShiftsBySite = [[]]*(self.Problem.totalPlaces)
        self.iteration = 0


    def ObtainComponents(self, canNewComponents):
        siteId = self.Problem.orderSitesForCantVigilantes[self.iteration]
        components = []
        shifts = self.obtainShiftBySite(self.Problem.getSite(siteId))
        vigilantsByPeriodInSite = self.Problem.cantVigilantsByPeriod[siteId-1]
        necesaryVigilantes = self.getNecesaryVigilants(siteId,vigilantsByPeriodInSite,shifts)
        for component in range(0,canNewComponents):
            component = Component(siteId,self.Problem.totalWeeks,vigilantsByPeriodInSite)
            self.getSchedule(component,shifts,copy.deepcopy(necesaryVigilantes))
            component.calcuteFitness()
            components.append(component)
        return components

    def getSchedule(self,component,shifts,necesaryVigilantes):
        listTempVigilant = []
        for shift in shifts:
            listTempVigilant.clear()
            for iteration in range(0,component.necesaryvigilantsByPeriod[shift[0]]):
                objViglant = self.obtainVigilantAvailable(shift[0],shift[1],listTempVigilant,necesaryVigilantes)
                if objViglant == None:
                    continue
                self.AssigmentVigilants(objViglant, component.siteId, shift,component)
                listTempVigilant.append(objViglant)
            self.updateHours(shift,listTempVigilant)
        
    def AssigmentVigilants(self, objVigilant, site, shift,component):
            if objVigilant not in component.assignedVigilants:
                component.assignedVigilants.append(objVigilant)
            for i in range(shift[0], shift[1]+1):
                objVigilant.setShift(i, site)
                component.siteSchedule[i].append(objVigilant.id)

    def updateHours(self,shift,lisVigilantsAssiged):
        for objVigilant in lisVigilantsAssiged:
            self.assigmentHoursVigilant(objVigilant,shift)

    def assigmentHoursVigilant(self, objVigilant,shift):
        for hours in range(shift[0],shift[1]+1):
            objVigilant.setHoursWorked(self.ShiftConvert(hours))

    def ShiftConvert(self, shift):
        week = 0
        while shift >= 168:
            shift = shift - 168
            week = week + 1
        return week
    
    def obtainVigilantAvailable(self, InitShift, endShift,assignedVigilantsInShift,vigilantList):
        ObjResultado = None
        for vigilants in vigilantList:
            indexVigilants = [*range(len(vigilants))]
            while indexVigilants:
                    rand = random.choice(indexVigilants)
                    objVigilant = vigilants[rand]
                    if objVigilant not in assignedVigilantsInShift and objVigilant.isVigilantAvailable(InitShift,endShift,self.Problem.maxWorkHoursPerWeek):
                        ObjResultado = objVigilant
                        return ObjResultado
                    indexVigilants.remove(rand)
        return ObjResultado

    def obtainShiftBySite(self,parSite):
        site = np.copy(parSite)
        working_day = []
        init = -1
        start = False
        k = 0
        for index, t in enumerate(site):
            if t == 0 and start == False:
                continue

            if t != 0:
                if init == -1:
                    init = index
                start = True
                if k<24:
                    k +=1

            if (t==0 and start == True) or k == 24:
                workindaytimes = self.Problem.workingDay[k]
                if workindaytimes == None:
                    print("el numero de horas no puede establecerce a un vigilantes revice EL DATASET")
                start = False
                if workindaytimes == 9:
                     return
                working_day = working_day + (self.calculateworkinday(workindaytimes,init))
                init = -1
                k = 0

        return working_day
     
    def calculateworkinday(self, workinday, indexWorkingDay):
        dayShiftS = []
        for durationShift in workinday:
            dayShiftS.append([indexWorkingDay,indexWorkingDay+durationShift-1])
            indexWorkingDay+=durationShift
        return dayShiftS
    
    def getNecesaryVigilants(self,siteId,vigilantsByPeriod,shifts):
        necesaryVigilantsByPeriodInAWeek = self.getNecesaryVigilantsByPeriodInAWeek(shifts,vigilantsByPeriod)
        cantNecesaryVigilantsInWeek = sum(necesaryVigilantsByPeriodInAWeek)
        porcentajeDeTrabajo = 3.5 #Un porcentaje obtenido de el trabajo promedio que se saca para una cantidad de turnos dependiendo de la cantidad usual de los dias que un guardia trabaja en el año
        cantVigilantsNecesaryInSite =  math.floor(cantNecesaryVigilantsInWeek/porcentajeDeTrabajo)
        expectedvigilantsInPlace = []
        orderVigilantsByDistance = []
        if siteId in self.Problem.vigilantExpectedPlaces:
            if len(self.Problem.vigilantExpectedPlaces[siteId]) >= cantVigilantsNecesaryInSite:
                expectedvigilantsInPlace = self.Problem.vigilantExpectedPlaces[siteId][:cantVigilantsNecesaryInSite].copy()
            else:
                expectedvigilantsInPlace = self.Problem.vigilantExpectedPlaces[siteId].copy()
            for iteration in range(0,len(expectedvigilantsInPlace)):
                expectedvigilantsInPlace[iteration] = self.vigilantsSchedule[expectedvigilantsInPlace[iteration]-1]
            cantVigilantsNecesaryInSite -= len(expectedvigilantsInPlace)
        if cantVigilantsNecesaryInSite > 0:
         orderVigilantsInPlaceByDistance = self.orderVigilantsInPlaceByDistance(self.vigilants,siteId)
         pos = 0
         while cantVigilantsNecesaryInSite > 0:
                if (orderVigilantsInPlaceByDistance[pos] in expectedvigilantsInPlace) == False:
                  orderVigilantsByDistance.append(self.vigilantsSchedule[orderVigilantsInPlaceByDistance[pos].id-1])
                  cantVigilantsNecesaryInSite-=1  
                pos+=1
        return [expectedvigilantsInPlace,orderVigilantsByDistance]
    
    def getNecesaryVigilantsByPeriodInAWeek(self,shifts,vigilantsByPeriod):
        vigilantsByPeriodInAWeek = []
        for shift in shifts:
            if shift[0] > 168:
                break 
            vigilantsByPeriodInAWeek.append(vigilantsByPeriod[shift[0]]) 
        return vigilantsByPeriodInAWeek
    
    def orderVigilantsInPlaceByDistance(self,vigilants,place):
        for iteration in range(0,len(vigilants)-1):
            swapped =False
            for pos in range(0,len(vigilants)-1-iteration):
                if(vigilants[pos + 1].distancesBetweenPlacesToWatch[place-1] < vigilants[pos].distancesBetweenPlacesToWatch[place-1]):
                    aux = vigilants[pos]
                    vigilants[pos] = vigilants[pos+1]
                    vigilants[pos + 1] = aux
                    swapped = True
            if swapped == False:
                break
        return vigilants 
    
    def BestComponents(self,components,cantRestrictedComponets):
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
            pass
        restrictedList = components[:cantRestrictedComponets]
        return restrictedList[random.randint(0,cantRestrictedComponets-1)]

    def Union(self, component):
        for vigilant in component.assignedVigilants:
            self.vigilantsSchedule[vigilant.id-1] = vigilant
            self.vigilantsForPlaces[component.siteId].append(vigilant)
        self.sitesSchedule[component.siteId-1] = component.siteSchedule
        self.missingShiftsBySite[component.siteId-1]  = component.missingShfits
        self.Fitness += component.fitness
        self.iteration+=1

    def CompleteSolution(self):
        if self.iteration < len(self.sitesSchedule):
            return True
        self.missingShiftsFormat(self.missingShiftsBySite)
        return False

    def generateResults(self,CurrentEFOs,MaxEFOs): 
        if CurrentEFOs == 0:
            self.Problem.generateResults('./Data/Results/FirstResult',self)
        elif CurrentEFOs == MaxEFOs/2:
            self.Problem.generateResults('./Data/Results/HalfResult',self)
        elif CurrentEFOs == MaxEFOs-1:
            self.Problem.generateResults('./Data/Results/FinalResult',self)

    def Tweak(self, solution):
        solution = self.tweakMissingShifts(solution,True)
        self.Problem.maxWorkHoursPerWeek = 56
        solution = self.tweakMissingShifts(solution,False)
        self.Problem.maxWorkHoursPerWeek = 48
        self.calculateFitness(solution)

        return solution
    
    def calculateFitness(self,solution):
        solution.Fitness = 0
        for site in range(0,len(solution.sitesSchedule)):
            for period in range(0,len(solution.sitesSchedule[site])):
                actualVigilants = len(solution.sitesSchedule[site][period])
                missingVigilants = self.Problem.cantVigilantsByPeriod[site][period] - actualVigilants
                solution.Fitness += missingVigilants*10000
        for vigilant in self.vigilantsSchedule:
            for assignedPlace in vigilant.shifts:
                if assignedPlace != 0:
                    #calculate fitness distance
                    if vigilant.expectedPlaceToWatch != assignedPlace:
                        solution.Fitness+= 500
                    #calculate work hours
                    for hourWeek in vigilant.HoursWeeks:
                        if hourWeek < 40 and hourWeek!=0:
                            solution.Fitness+= 800
                        if hourWeek > 48:
                            solution.Fitness+= 300
                    #Calculate preferencias 
                    #TODO 

    def tweakMissingShifts(self,solution, order):
        solution = self.tweakMissingHoursVigilants(solution)
        solution = self.tweakVigilants(solution)
        return solution
    def getVigilantsForPlaceList(self,vigilantsForPlace):
        listSite = []
        for site in vigilantsForPlace:
            listSite.append(vigilantsForPlace[site])
        return  listSite

    def getAleatory(self,parInit,parEnd,parNumber):
        '''
        generate n number aleatory between  nunber init and number end
        :param init: number init
        :param end: number end
        :param number: quantity the number aleatory
        :return: list number aleatory
        '''
        k= 0
        listAleatory = []
        while True:
            if parNumber > k:
                numAleatory = random.randint(parInit,parEnd)
                if numAleatory not in listAleatory:
                    listAleatory.append(numAleatory)
                    k=k+1
            else:
                break
        return  listAleatory

    def toExchageVigilants(self,parIdSiteOne,parIdVigilantOne,parIdSiteTwo,parIdVigilantsTwo,solucion):
        '''
        to Exchage vigilants between sites
        :param parSiteOne: site one select ramdoly
        :param parVigilantOne: vigilant one select the site one ramdoly
        :param parSiteTwo:
        :param parVigilantsTwo:
        :return: None
        '''
        try:
            objVigilantOne = solucion.vigilantsForPlaces.get(parIdSiteOne)[parIdVigilantOne]
            objVigilantTwo = solucion.vigilantsForPlaces.get(parIdSiteOne)[parIdVigilantOne]
            self.updateFitnees(objVigilantOne, parIdSiteOne, parIdSiteTwo, solucion)
            self.updateFitnees(objVigilantTwo, parIdSiteTwo, parIdSiteOne, solucion)
            temVigilanOne = solucion.vigilantsForPlaces.get(parIdSiteOne)[parIdVigilantOne]
            solucion.vigilantsForPlaces.get(parIdSiteOne)[parIdVigilantOne] = solucion.vigilantsForPlaces.get(parIdSiteTwo)[parIdVigilantsTwo]
            solucion.vigilantsForPlaces.get(parIdSiteTwo)[parIdVigilantsTwo] = temVigilanOne
        except:
            print("excption")

    def updateFitnees(self,objVigilants:Vigilant,site,newSite,solucion):
        solucion.Fitness -= objVigilants.distancesBetweenPlacesToWatch[site]
        solucion.Fitness += objVigilants.distancesBetweenPlacesToWatch[newSite]

    def tweakVigilants(self,solucion):
        if self.is_empty(solucion.vigilantsForPlaces):
            listSite = self.getAleatory(1, len(solucion.vigilantsForPlaces), 2)
            vigilantOne = self.getAleatory(0, len(solucion.vigilantsForPlaces[listSite[0]]), 1)
            vigilantTwo = self.getAleatory(0, len(solucion.vigilantsForPlaces[listSite[1]]), 1)
            self.toExchageVigilants(listSite[0], vigilantOne[0], listSite[1], vigilantTwo[0], solucion)
        return solucion

    def is_empty(self,list):
        varResult = True
        for i in list:
            if list.get(i) == [] :
                varResult = False
                break
        return varResult

    def tweakMissingHoursVigilants(self,solution):
        vigilantsByHours = self.GetVigilatsByHours(solution.vigilantsSchedule)
        vigilantsByHours= collections.OrderedDict(sorted(vigilantsByHours.items(),reverse=order))
        listTempVigilant = []
        for indexSite in range(0,len(self.missingShiftsBySite)):
            for shift in  self.missingShiftsBySite[indexSite]:
                listTempVigilant.clear()
                cantNecessariVigilantsInShift = self.Problem.cantVigilantsByPeriod[indexSite][shift[0]] - len(self.sitesSchedule[indexSite][shift[0]])
                numberIterations = cantNecessariVigilantsInShift
                for i in range(0,numberIterations):
                    objViglant = self.obtainVigilantAvailable(shift[0],shift[1],listTempVigilant,vigilantsByHours.values())
                    if objViglant == None:
                        continue
                    objViglant.setShifts(shift, indexSite+1)
                    cantNecessariVigilantsInShift-=1
                    for i in range(shift[0],shift[1]+1):
                        solution.sitesSchedule[indexSite][i].append(objViglant.id)
                        #solution.Fitness-=10000
                    listTempVigilant.append(objViglant)
                if cantNecessariVigilantsInShift == 0:
                    self.missingShiftsBySite[indexSite].remove(shift)
                self.updateHours(shift,listTempVigilant)
                # for vigilan in listTempVigilant:
                #     for week in vigilan.HoursWeeks:
                #         if week > 48:
                #             solution.Fitness+= (week-48)*100
        return solution
    

        
    def missingShiftsFormat(self,missingShiftsBySite):
        shiftsFormat = []
        for missingShiftsInSite in missingShiftsBySite:
            shifts = []
            nHoras = 0
            if missingShiftsInSite:
                indexShift = 0
                cantMissingShifts = len(missingShiftsInSite)
                for i in range(0,cantMissingShifts-1):
                    if missingShiftsInSite[i]+1 != missingShiftsInSite[i+1] or nHoras == 23 or i == cantMissingShifts-2:
                       
                        nHoras+=1
                        shifts  = shifts + self.calculateworkinday(self.Problem.workingDay[nHoras],missingShiftsInSite[indexShift])
                        indexShift+= nHoras
                        nHoras = 0
                    else:
                        nHoras+=1
                shifts[len(shifts)-1][1] +=1
            shiftsFormat.append(shifts)
        self.missingShiftsBySite = shiftsFormat


    def GetVigilatsByHours(self,vigilants):
        vigilantByHours = {}
        for vigilant in vigilants:
            if vigilant.HoursWorked in vigilantByHours:
                vigilantByHours[vigilant.HoursWorked].append(vigilant)
            else:
                vigilantByHours[vigilant.HoursWorked] = [vigilant]
        return vigilantByHours