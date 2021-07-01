from Turno import  Turno
import numpy as np
import math
class Vigilant:

    def __init__(self,id, expectedPlace,preferences,distances,numberWeek):
        self.id = id
        self.HoursofRest = 0
        self.HoursWorked = 0
        self.distances = distances
        self.expectedPlace = expectedPlace
        self.preferences = preferences
        self.shifts = np.zeros(168*numberWeek)
        self.HoursWeeks = np.zeros(numberWeek)      
   
    def isVigilantAvailable(self,startPeriod,endPeriod):
        if self.hasEnoughHoursToWork(startPeriod,endPeriod) == False:
            return False
        if self.availabilityShift(startPeriod,endPeriod) == False:
            return False
        if self.enoughResting(startPeriod) == False:
            return False
        week = math.floor(startPeriod/168)
        if (startPeriod > 144+ (168*week) and startPeriod < 168*(week+1)):
            return self.workInLastSunday(week)
        else:
            if (endPeriod > 144+ (168*week)):
                return self.workInLastSunday(week)
        return True
    
    def availabilityShift(self,startPeriod,endPeriod):
        for period in range(startPeriod,endPeriod):
            if self.shifts[period] != 0:
                return False
        return True


        
    def hasEnoughHoursToWork(self,startPeriod,endPeriod):
        # startPeriod = 328
        # endPeriod = 336
        weekStarPeriod = math.floor(startPeriod/168)
        weekEndPeriod  =  math.floor(endPeriod/168)
        if weekStarPeriod == weekEndPeriod:
            if  (self.HoursWeeks[weekStarPeriod]+(endPeriod - startPeriod)) <= 56:
                return True
            return False
        else:
            if (self.HoursWeeks[weekStarPeriod]+(168*weekEndPeriod)-startPeriod) <= 56 and (self.HoursWeeks[weekEndPeriod]+endPeriod-(168*weekEndPeriod)) <= 56:
                return True
        return False
    
    def setShift(self, index, site):
        self.shifts[index] = site

    def workInLastSunday(self,week):
        if week == 0:
            return False
        for period in range (168*week,(168*week)-24,-1):
            if self.shifts[period] != 0:
                return True
        return False
    def setHoursWorked(self,week):
        self.HoursWeeks[week] = self.HoursWeeks[week]+1
    def setHoursRest(self, hours):
        self.HoursofRest = self.HoursofRest + hours