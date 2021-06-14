import numpy as np
import pandas as pd
from File import File
from VigilantsFile import VigilantsFile
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
    cantVigilantsPeriod = []
    vigilantes = []
    dataSetVigilants = []
    
    def __init__(self, pathInterface , pathVigilants, weeks):
        self.totalWeeks = weeks
        self.totalPeriods = 168*self.totalWeeks
        self.identifiesWeekStartPeriod()
        self.readData(pathInterface,pathVigilants)
        self.initProblem()
        self.createShift(self.Dataset)

    def readData(self, pathInterface , pathVigilants):
        datasets = File(pathInterface, self.totalWeeks)
        self.Dataset = datasets.DataProblem
        self.totalPlaces = len(self.Dataset)
        for place in self.Dataset:
            cantVigilantByPeriod = []
            for cantByperiod in place:
                cantVigilantByPeriod.append(cantByperiod)
            self.cantVigilantsPeriod.append(cantVigilantByPeriod)
        #Read Vigilant data
        data = VigilantsFile(pathVigilants)
        self.dataSetVigilants = data.vigilantesInfo
        self.totalVigilantes = data.numberVigilants

    def initProblem(self):
        '''
        inicialize empty default problem
        :return: None
        '''
        #init vigilantes and shift default
        for i in range(self.totalVigilantes):
            objVigilant = Vigilant(self.totalWeeks,self.dataSetVigilants[i][0],self.dataSetVigilants[i][1],self.dataSetVigilants[i][2])
            self.vigilantes.append(objVigilant)


    def createShift(self, dataSet):
        '''
        Assigment vigilant to a shift and site
        :param dataSet: data the input shift for to vigilantes
        '''
        while self.Site < self.totalPlaces:
            while self.Shift < self.totalPeriods:
                sites = []
                if dataSet[self.Site][self.Shift] != 0:
                    self.assigmentVigilantes(self.aleatoryVigilantes(dataSet[self.Site][self.Shift], 0, self.totalVigilantes-1))
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

    def aleatoryVigilantes(self, numVigilantes, numInit, numEnd):
        vigilantList = []
        while len(vigilantList) < numVigilantes:
            aleatoryVigilant=random.randint(numInit, numEnd)
            if aleatoryVigilant is not vigilantList:
                vigilantList.append(aleatoryVigilant)
        return  vigilantList

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
                self.addVigilantShift(i, week, turno, self.Site, 1)

    def addvigilant(self):
        if self.Shift < self.totalPeriods:
            turno, week = self.ShiftConvert(self.Shift)  # trasformation the shift a shift and week
            self.addVigilantShift(random.randint(0, self.totalVigilantes), week, turno, self.Site, 1)

    def addVigilantShift(self, Indexvigilant, IndexWeek, IndexTurno, indexSite, state):
        #validate if the vigilant is on shift
        k = 0
        while k < self.totalVigilantes:

            vigilantIs=self.validateVigilantinShift(Indexvigilant, IndexWeek, IndexTurno)
            if not vigilantIs:
                self.vigilantes[Indexvigilant].shifts[IndexWeek][IndexTurno].state = state  # vigilantes
                self.vigilantes[Indexvigilant].shifts[IndexWeek][IndexTurno].site = indexSite
                self.vigilantes[Indexvigilant].shifts[IndexWeek][IndexTurno].assigmentVigilantes.append(Indexvigilant)
                break
            Indexvigilant=random.randint(0, self.totalVigilantes)
            k += 1



    def validateVigilantinShift(self, IndexVigilant, IndexWeek, IndexTurno):
        vigilantIs = False
        vigilantes=self.vigilantes[IndexVigilant].shifts[IndexWeek][IndexTurno].assigmentVigilantes
        if IndexVigilant is vigilantes:
            vigilantIs = True
        return vigilantIs

    def to_Save(self, path):
        result = np.empty((0, self.totalPeriods) ,int)
        for vigilantI, vigilant in enumerate(self.vigilantes):
            turno = self.getShitfVigilant(vigilant)
            #turno.insert(0, vigilantI)
            result = np.append(result, np.array([turno]), axis=0)
        result = pd.DataFrame(result)
        result.to_csv(path)


    def getShitfVigilant(self, vigilant):
        turno = []
        for weekI, week in enumerate(vigilant.shifts):
            for shiftI, shift in enumerate(week):
                turno.append(shift.state)
        return turno


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
    def evalute2(self, solution):
        vigilantsByPeriod = self.cantVigilantsPeriod.copy()
        fitness = 0
        for vigilant in solution:
            period = 0
            hoursWorking = 0
            isVigilanResting = True
            restTime = self.minBreakDuration + 1
            day = 1
            weekToCheck = 1
            workInSunday = False
            for week in range(0,len(vigilant.shifts)):
                for periodInWeek in range(0,len(vigilant.shifts[week])):
                    place = vigilant.shifts[week][periodInWeek].site
                    if place != 0 and place != None:
                        #Verifica que existe el turno
                        if self.cantVigilantsPeriod[place][period] == 0:
                            print("El turno en el periodo " + str(periodInWeek) +" de la semana "+ str(week)+ " en el lugar "+str(place)+" no existe "+str(self.cantVigilantsPeriod[place][period]))
                            fitness+=1000
                        #Verifica horas de descanso
                        if restTime < self.minBreakDuration and isVigilanResting:
                            fitness+= 1000
                            print("No se cumplieron las horas necesarias de descando del guardia "+str(restTime))
                        isVigilanResting = False
                        restTime = 0 
                        hoursWorking +=1
                        vigilantsByPeriod[place][period]-=1
                        #verifica que no se hagan cambios entre las 11p.m y 5p.m
                        if 23*day + (day-1) <= period and period <30*day - ((day-1)*6):
                            if vigilant.shifts[week][periodInWeek-1].site == None:
                                print("No se puede hacer cambios entre las 11 y 5: Periodo "+ str(periodInWeek) + " Semama "+ str(week))
                                fitness+= 100
                        #Verifica si trabajo dos domingo consecutivos
                        if weekToCheck == week+1 and period  >= 144 + week*168 and period <= 168 * (week+1):
                            if workInSunday:
                                fitness+= 100
                                print("Un guardia no puede trabajr dos domingos consecutivos week "+str(week-1)+" nextWeek " +str(week))
                            workInSunday = True
                            weekToCheck = week+2
                    else:
                        #Verifica las horas seguidas trabajadas
                        if hoursWorking < self.minShiftDuration and isVigilanResting == False:
                            fitness += (self.minShiftDuration - hoursWorking)*1000
                            print("Un guardia debe trabajar un minimo de horas "+str(hoursWorking))
                        if hoursWorking >  self.maxShiftDuration and isVigilanResting == False:
                            fitness += (hoursWorking - self.maxShiftDuration)*1000
                            print("Un guardia debe trabajar un maximo de horas "+str(hoursWorking))
                        isVigilanResting = True
                        restTime +=1
                        hoursWorking = 0
                    if period >= 30 + (24*(day-1)):
                        day +=1 
                    period+=1
                if weekToCheck == week:
                    workInSunday = False
                #NO debe exceder la cantidad de horas extras trabajadas
                if(vigilant.HoursWeeks[week] > self.maxWorkHoursPerWeek):
                    fitness += 500
                    print("No se deben superar la cant de horas semanales:"+str(vigilant.HoursWeeks[week]))
                #Se debe trabajar u minimo d horas trabajadas
                if(vigilant.HoursWeeks[week] < self.maxWorkHoursPerWeek):
                    fitness += 500
                    print("se debe trabar un min cant de horas semanales:"+str(vigilant.HoursWeeks[week]))
        #verificar catidad de guardias
        locPlace = 0
        for place in vigilantsByPeriod:
            for period in place:
                if period != 0:
                    fitness+= abs(period)*1000
                    #print("Se deben cumplir la cant de guardias para el sitio "+str(locPlace)+" en el periodo " +str(period))
            locPlace+=1    
