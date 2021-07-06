from Component import Component
from heapq import merge
from Site import Site
from random import random
import random
import Vigilant
import math
import numpy as np
from Algorithm import Algorithm
from VigilantAssigment import VigilantAssigment
import copy 
random.seed(0)

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

        self.vigilantsForPlaces = {}
        self.initVigilsForPlaces()
        self.vigilants = self.Problem.vigilantes.copy()
        
    def initVigilsForPlaces(self):
        sites = self.Problem.orderSitesForCantVigilantes
        for site in sites:
            self.vigilantsForPlaces[site] = []

        self.schedule = [None]*(len(self.Problem.vigilantes))
        self.sitesSchedule = [None]*(self.Problem.totalPlaces)



    def Tweak(self, Problem):

        # implementation
        return 0
    def ObtainComponents(self):
        siteId = self.Problem.orderSitesForCantVigilantes[0]
        canNewComponents = 3
        components = []
        #todo: tener en cuenta las horas de descanzo no cesariamente pueden ser consecutivas???
        shifts = self.obtainShiftBySite(self.Problem.getSite(siteId)) #retorna listado de jornadas para el sitio N
        vigilantsByPeriodInSite = self.Problem.cantVigilantsPeriod[siteId-1].copy()
        necesaryVigilantes = self.getNecesaryVigilants(siteId,vigilantsByPeriodInSite,shifts)
        for component in range(0,canNewComponents):
            component = Component(self.schedule,siteId,self.Problem.totalWeeks,vigilantsByPeriodInSite)
           # v = copy.copy(necesaryVigilantes[0][0])
            self.getSchedule(component,shifts,copy.deepcopy(necesaryVigilantes))
            component.calcuteFitness()
            components.append(component)
        return components


    def getSchedule(self,component,shifts,necesaryVigilantes):
        listTempVigilant = []
        for shift in shifts:
            listTempVigilant.clear()
            for iteration in range(0,component.vigilantsByPeriod[shift[0]]): #todo: encontra una forma mas segura
                objViglant = self.obtainVigilantAvailable(component.siteId,shift[0],shift[1],listTempVigilant,necesaryVigilantes)
                self.AssigmentVigilants(objViglant, component.siteId, shift,component)
                listTempVigilant.append(objViglant.id) #guardos los vigilantes que se van asignado al sitio
            self.updateHours(shift,listTempVigilant,component.siteId)
        

    def AssigmentVigilants(self, objVigilant, site, shift,component):
            for i in range(shift[0], shift[1]+1):
                objVigilant.setShift(i, site)
                component.siteSchedule[i].append(objVigilant.id)

    def updateHours(self,shift,lisVigilantsAssiged,site):
        hoursWorkend = self.obtainRange(shift[0], shift[1])
        #asigna horas de descanso a los vigilantes que este trabajando en el sitio y ya se le hallan asignado un turno
        for idVigilant in self.vigilantsForPlaces[site]:
            objVigilant = self.Problem.getVigilant(idVigilant)
            self.assigmentHoursVigilant(objVigilant, hoursWorkend, 'rest')

        self.updateListVigilanteforSite(site,lisVigilantsAssiged)

       #asigna horas de trabajo a los vigilantes los cuales apenas se les asigno turno en la itercion anterior
        for idVigilant in lisVigilantsAssiged:
            objVigilant = self.Problem.getVigilant(idVigilant)
            self.assigmentHoursVigilant(objVigilant,hoursWorkend,'worked')

    def updateListVigilanteforSite(self,site,listVigilantnew):
        """
         # se actualiza los vigilantes que estan trabajando en el sitio
        """
        vigilants = self.vigilantsForPlaces[site]
        vigilants.extend(element for element in listVigilantnew if element not in vigilants)
        #vigilants = list(merge(vigilants,listVigilantnew))
        #vigilants = listVigilantnew + vigilants
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
    def CompleteSolution(self):
        # implementation
        return 1
    def aleatory(self,init, end):
        return random.randint(init, end)
    def assignVigilantsmissingofSite(self, siteId):
        workingday = self.Problem.workingDay(siteId)
    def obtainVigilantAvailable(self,site, InitShift, endShift,lisVigilantDefault,vigilantDefaultList):

        #todo: optimizar metodo, posible mente dividir en dos metodos y revisar la validacion de inexistencia de vigilants repetidos
        ObjResultado = None
        #1 vigilante de los asignados al sitio
        for i in range(0,100):
            if i == 98:
                print("encontrado")
            #todo : revisar el limite superios del for, cuentas iteraciones se podrian hacer en caso de que no encuentr un vigilantes valido??
            #vigilantDefaultList =self.Problem.vigilantExpectedPlaces[site]
            objVigilant = random.choice(vigilantDefaultList[0]) #toma un elemento de forma aleatorio de la lista
            if objVigilant.isVigilantAvailable(InitShift,endShift) and objVigilant not in lisVigilantDefault:
                ObjResultado = objVigilant
                return ObjResultado

        #2 si no existe vigilante valido dentro del sitio se toma uno de la lista de vigilantes global y se asigna a la lista de vigi
        #lantes para el sitio
        for j in range(0,len(vigilantDefaultList[1])):
            objVigilant = random.choice(vigilantDefaultList[1])
            if objVigilant.isVigilantAvailable(InitShift,endShift) and objVigilant not in lisVigilantDefault:
                ObjResultado = objVigilant
                return ObjResultado
        if ObjResultado == None:
            print("no se encontraron mas vigilantes validos")
            exit()

        return ObjResultado
       # return True if self.sitesSchedule[len(self.sitesSchedule)-1] == None else False

    def obtainShiftBySite(self,parSite):
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
    def OrderSitesForCantVigilantes(self, problem):
        return 1
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
        self.updateListVigilanteforSite(component)
        for vigilant in component.newVigilants:
            self.schedule[vigilant.id-1] = vigilant
        self.sitesSchedule[component.siteId-1] = component.siteSchedule

    def orderVigilantsBySite(self,place):
        for iteration in range(0,len(self.vigilants)-1):
            swapped =False
            for pos in range(0,len(self.vigilants)-1-iteration):
                if(self.vigilants[pos + 1].distances[place-1] < self.vigilants[pos].distances[place-1]):
                    aux = self.vigilants[pos]
                    self.vigilants[pos] = self.vigilants[pos+1]
                    self.vigilants[pos + 1] = aux
                    swapped = True
            if swapped == False:
                break
        return self.vigilants 

    def getNecesaryVigilants(self,siteId,vigilantsByPeriod,shifts):
        vigilantsByPeriodInAWeek = self.getVigilantsByPeriodInAWeek(shifts,vigilantsByPeriod,)
        cantNecesaryVigilantsInWeek = sum(vigilantsByPeriodInAWeek)
        #cantNecesaryVigilantsInWeek = 100
        porcentajeDeTrabajo = 3.5 #Un porcentaje obtenido de el trabajo promedio que se saca para una cantidad de turnos dependiendo de la cantidad usual de los dias que un guardia trabaja en el año
        canVigilantsNecesaryInSite =  math.floor(cantNecesaryVigilantsInWeek/porcentajeDeTrabajo)
        Expectedvigilants = []
        orderVigilants = []
        if siteId in self.Problem.vigilantExpectedPlaces:
            if len(self.Problem.vigilantExpectedPlaces[siteId]) >= canVigilantsNecesaryInSite:
                Expectedvigilants = self.Problem.vigilantExpectedPlaces[siteId][:canVigilantsNecesaryInSite]
            else:
                Expectedvigilants = self.Problem.vigilantExpectedPlaces[siteId]
            canVigilantsNecesaryInSite -= len(Expectedvigilants)
        if canVigilantsNecesaryInSite > 0:
         orderVigilantsBySite = self.orderVigilantsBySite(siteId)
         pos = 0
         while canVigilantsNecesaryInSite > 0:
                if (orderVigilantsBySite[pos] in Expectedvigilants) == False:
                  orderVigilants.append(orderVigilantsBySite[pos])
                  canVigilantsNecesaryInSite-=1  
                pos+=1
        return [Expectedvigilants,orderVigilants]
    def getVigilantsByPeriodInAWeek(self,shifts,vigilantsByPeriod):
        vigilantsByPeriodInAWeek = []
        for shift in shifts:
            if shift[0] > 168:
                break 
            vigilantsByPeriodInAWeek.append(vigilantsByPeriod[shift[0]]) 
        return vigilantsByPeriodInAWeek