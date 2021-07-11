from Component import Component
from random import random
import random
import math
import numpy as np
from Algorithm import Algorithm
from VigilantAssigment import VigilantAssigment
import copy 

random.seed(0)

class Solution:

    sitesSchedule = []
    vigilantsSchedule = []
    Fitness = int
    MyContainer = Algorithm
    Problem = VigilantAssigment
    vigilantsForPlaces = None
    

    def __init__(self, theOwner, Aletory):
        self.MyContainer = theOwner
        self.MyContainer.Aleatory = Aletory
        self.Problem = self.MyContainer.VigilantAssigment
        self.vigilantsForPlaces = {}
        self.initVigilsForPlaces()
        self.vigilantsSchedule = self.Problem.vigilantes.copy()
        self.vigilants = self.Problem.vigilantes.copy()
        self.iteration = 0
        
    def initVigilsForPlaces(self):
        sites = self.Problem.orderSitesForCantVigilantes
        for site in sites:
            self.vigilantsForPlaces[site] = []
        self.sitesSchedule = [[]]*(self.Problem.totalPlaces)

    def ObtainComponents(self):
        siteId = self.Problem.orderSitesForCantVigilantes[self.iteration]
        canNewComponents = 3
        components = []
        shifts = self.obtainShiftBySite(self.Problem.getSite(siteId))
        vigilantsByPeriodInSite = self.Problem.cantVigilantsPeriod[siteId-1]
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
            self.updateHours(shift,listTempVigilant,component.siteId)
        
    def AssigmentVigilants(self, objVigilant, site, shift,component):
            if objVigilant not in component.assignedVigilants:
                component.assignedVigilants.append(objVigilant)
            for i in range(shift[0], shift[1]+1):
                objVigilant.setShift(i, site)
                component.siteSchedule[i].append(objVigilant.id)

    def updateHours(self,shift,lisVigilantsAssiged,site):
        hoursWorkend = self.obtainRange(shift[0], shift[1])
        for objVigilant in self.vigilantsForPlaces[site]:
            self.assigmentHoursVigilant(objVigilant, hoursWorkend, 'rest')
        self.updateListVigilanteforSite(site,lisVigilantsAssiged)

        for objVigilant in lisVigilantsAssiged:
            self.assigmentHoursVigilant(objVigilant,hoursWorkend,'worked')

    def updateListVigilanteforSite(self,site,listVigilantnew):
        vigilants = self.vigilantsForPlaces[site]
        vigilants.extend(element for element in listVigilantnew if element not in vigilants)
        self.vigilantsForPlaces[site] = vigilants

    def assigmentHoursVigilant(self, objVigilant,hoursWorkend,typeHours):
        if typeHours == "rest":
            for hours in hoursWorkend:
                objVigilant.setHoursRest(self.ShiftConvert(hours))
        if typeHours == "worked":
            for hours in hoursWorkend:
                objVigilant.setHoursWorked(self.ShiftConvert(hours))

    def ShiftConvert(self, shift):
        week = 0
        while shift >= 168:
            shift = shift - 168
            week = week + 1
        return week
    
    def obtainVigilantAvailable(self, InitShift, endShift,lisVigilantDefault,vigilantDefaultList):
        #busca en la lista de vigilantes por default [0](vigilantes fijos) si hay disponibles para asignar
        ObjResultado = None
        for i in vigilantDefaultList[0]:
                objVigilant = random.choice(vigilantDefaultList[0])
                if objVigilant.isVigilantAvailable(InitShift,endShift) and objVigilant not in lisVigilantDefault:
                    ObjResultado = objVigilant
                    return ObjResultado
        #busca en la lista de vigilantes por default [1](ordenados por distancia) si hay disponibles para asignar
        for j in vigilantDefaultList[1]:
            objVigilant = random.choice(vigilantDefaultList[1])
            if objVigilant.isVigilantAvailable(InitShift,endShift) and objVigilant not in lisVigilantDefault:
                ObjResultado = objVigilant
                return ObjResultado
        if ObjResultado == None:
            print("no se encontraron mas vigilantes validos")

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
                working_day = working_day + (self.calculateworkinday(workindaytimes,init,index))
                init = index+1
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
    
    def obtainRange(self, numberInit, numberEnd):
        shift = []
        while numberInit <= numberEnd:
            shift.append(numberInit)
            numberInit +=1
        return shift
    
    def UpdateListVigilantAvaliable(self,components):
        Listvigilants=self.vigilantsForPlaces[components.siteId]
        for i in Listvigilants:
            self.vigilants.remove(i)    

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
            pass
        restrictedList = components[:5]
        return restrictedList[random.randint(0,cantRestrictedComponets-1)]

    def Union(self, component):
        for vigilant in component.assignedVigilants:
            self.vigilantsSchedule[vigilant.id-1] = vigilant
        self.sitesSchedule[component.siteId-1] = component.siteSchedule
        self.iteration+=1

    def CompleteSolution(self):
        if self.iteration < len(self.sitesSchedule):
            return True
        return False

    def generateResults(self,CurrentEFOs,MaxEFOs): 
        if CurrentEFOs == 0:
            self.Problem.generateResults('./Data/Results/FirstResult',self)
        elif CurrentEFOs == MaxEFOs/2:
            self.Problem.generateResults('./Data/Results/HalfResult',self)
        elif CurrentEFOs == MaxEFOs-1:
            self.Problem.generateResults('./Data/Results/FinalResult',self)

    def Tweak(self, Problem):

        # implementation
        return 0