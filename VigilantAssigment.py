from Turno import *

class VigilantAssigment:
    totalVigilants =0
    totalPlaces=0
    totalWeeks=0
    totalPeriods=0
    maxShiftDuration=0
    minShiftDuration=0
    minBreakDuration=0
    maxOvertimeWorkHoursPerWeek=0
    maxWorkHoursPerWeek=0
    minWorkHoursPerWeek=0
    idealWorkHoursPerWeek=0
    vigilantDistance=0
    vigilantPreference=0
    shifts = [] # 0[turnos,turnos...] [1]
    periodEndWeek = []
    turnosAsignados = []
    
    def __init__(self,dataSet,weeks):
        self.totalVigilants = 1
        self.totalPlaces = len(dataSet)
        self.totalWeeks = weeks
        self.totalPeriods = 24*7*self.totalWeeks
        self.maxShiftDuration = 12
        self.minShiftDuration = 6
        self.minBreakDuration = 18
        self.maxOvertimeWorkHoursPerWeek = 12
        self.maxWorkHoursPerWeek = 48
        self.minWorkHoursPerWeek = 40
        self.idealWorkHoursPerWeek = 48
        #Identifica el periodo de inicio de la semana
        for i in range(0,self.totalWeeks):
            self.periodEndWeek.append((i+1)*168)
        #Creacion de turnos    
        for i in range(0,self.totalPlaces):
            shifts = []
            for j in range(0,168*self.totalWeeks):
                shifts.append(Turno(dataSet[i][j]))
            self.shifts.append(shifts)
    def addVigilant(self,place,period,vigilant):
        self.shifts[place][period].addVigilant(vigilant)
    def getShifts(self):
        return self.turnosAsignados
    def getCantPlaces(self):
        return self.totalPlaces        
    def evalute(self, solution):
        fitness = 0
        isVigilanResting = True
        hoursWorking = 0
        restTime = self.minBreakDuration + 1
        for vigilant in range(0,self.totalVigilants):
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

                
