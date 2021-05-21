import numpy as np

from Turno import *
from Vigilant import Vigilant
import random

class VigilantAssigment:
    totalVigilantes = 30
    totalPlaces=0
    totalWeeks=0
    totalPeriods=0
    maxShiftDuration=12
    minShiftDuration=6
    minBreakDuration=18
    maxOvertimeWorkHoursPerWeek=12
    maxWorkHoursPerWeek=48
    minWorkHoursPerWeek=40
    idealWorkHoursPerWeek=48
    vigilantDistance=0
    vigilantPreference=0
    Sites = []
    VigilantesList = []
    Shifts = []
    periodEndWeek = []
    Site = 0
    Shift = 0
    turnosAsignados = []
    vigilantes = []
    
    def __init__(self, dataSet, weeks):
        self.totalPlaces = len(dataSet)
        self.totalWeeks = weeks
        self.totalPeriods = 168*self.totalWeeks
        self.identifiesWeekStartPeriod()
        self.Dataset = dataSet
        self.initProblem()
        self.createShift(dataSet)

    def initProblem(self):
        '''
        inicialize empty default problem
        :return: None
        '''
        #init vigilantes and shift default
        for i in range(self.totalVigilantes):
            objVigilant = Vigilant(self.totalWeeks)
            self.vigilantes.append(objVigilant)


    def createShift(self, dataSet):
        '''
        Assigment vigilant to a shift and site
        :param dataSet: data the input shift for to vigilantes
        '''
        while self.Site < self.totalPlaces:
            while self.Shift < self.totalPeriods:
                sites = []
                if dataSet[self.Site][self.Shift] != 0 :
                    self.assigmentVigilantes(self.aleatoryVigilantes(dataSet[self.Site][self.Shift]))
                self.Shift += 1
            self.Shift = 0
            if sites:
                self.Shifts.append(sites)
            self.Site += 1


    def assigmentVigilantes(self, vigilantes):
        '''
        assigna of vigilantes to site in shift
        :param site: index site
        :param shift: index shift of site
        :param vigilantes: list vigilantes assigment
        :return:
        '''
        for i in range(8): #todo: 8 numero aleatorio
            self.addVigilant(vigilantes)
            self.Shift += 1

    def aleatoryVigilantes(self, numVigilantes):
        vigilantList = []
        for i in range(numVigilantes):
            vigilantList.append(random.randint(0, self.totalVigilantes-1))#todo se puede genear valores repetidos
        return vigilantList

    def identifiesWeekStartPeriod(self):
        '''
        identify the shift the init for the week
        '''
        for i in range(0, self.totalWeeks):
            self.periodEndWeek.append((i + 1) * 168)

    def ShiftConvert(self, shift):
        i = 0
        while shift >= 168:
            shift = shift - 168
            i = i + 1
        return shift, i

    def addVigilant(self, vigilantes):
        for i in vigilantes:
            if self.Shift < self.totalPeriods:
                turno, week = self.ShiftConvert(self.Shift)  # trasformation the shift a shift and week
                self.vigilantes[i].shifts[week][turno].state = 1 #vigilantes
                self.vigilantes[i].shifts[week][turno].site = self.Site
    def to_print(self):
        result =  []
        for vigilantI, vigilant in enumerate(self.vigilantes):
            for weekI, week in enumerate(vigilant.shifts):
                for shiftI, shift in enumerate(week):
                    result[vigilantI][]



    def getShifts(self):
        return self.turnosAsignados

    def getCantPlaces(self):
        return self.totalPlaces

    def evalute(self, solution):
        fitness = 0
        isVigilanResting = True
        hoursWorking = 0
        restTime = self.minBreakDuration + 1
        for vigilant in range(0, self.totalVigilantes):
            cantWorkHoursWeek = 0
            day = 1
            week =1
            weekToCheck = 1
            workInSunday = False
            for period in range(0,self.totalPeriods):
                place = solution[vigilant][period]-1
                if place > -1:
                    isVigilanResting = False
                    #Verifica horas de descanso
                    if restTime < self.minBreakDuration:
                        fitness+= 1000
                    restTime = 0 
                    hoursWorking +=1
                    cantWorkHoursWeek += 1
                    shift = self.shifts[place][period]
                    #verifica si existe el turno            
                    if(shift.getCantVigilantsPerPeriod() == 0 and place != 0):
                        fitness+= 5000
                    #verifica si extan la cantidad de guardias            
                    fitness += abs((shift.getCantAssigmentVigilants() - shift.getCantVigilantsPerPeriod())*1000)
                    #verifica que no se hagan cambios entre las 11p.m y 5p.m
                    if 23*day + (day-1) <= period and period <30*day - ((day-1)*6):
                        if self.shifts[place][period-1] == 0:
                            fitness+= 100
                    #Verifica si trabajo dos domingo consecutivos
                    if weekToCheck == week and period  >= 144 + (week-1)*168 and period <= 168 * week:
                        if workInSunday:
                            fitness+= 100
                        workInSunday = True
                        weekToCheck = week+1
                else:
                    #Verifica las horas seguidas trabajadas
                    if hoursWorking < self.minShiftDuration and isVigilanResting == False:
                        fitness += (self.minShiftDuration - hoursWorking)*1000
                    if hoursWorking >  self.maxShiftDuration and isVigilanResting == False:
                        fitness += (hoursWorking - self.maxShiftDuration )*1000
                    if weekToCheck == week:
                        workInSunday = False
                    isVigilanResting = True
                    restTime +=1
                    hoursWorking = 0

                if period >= 30 + (24*(day-1)):
                    day +=1    
                #Verifica que No se pase de las horas trabajadas por semana
                if(period in self.periodEndWeek):
                    if(cantWorkHoursWeek > self.maxWorkHoursPerWeek):
                         fitness += 500
                    if(cantWorkHoursWeek < self.minWorkHoursPerWeek):
                         fitness += 500
                    cantWorkHoursWeek = 0
                    week+=1
            return fitness

                
