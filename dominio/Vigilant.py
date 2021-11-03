import numpy as np
import math
class Vigilant:

    def __init__(self,id, expectedPlaceToWatch,shiftPreferences,distancesBetweenPlacesToWatch,numberWeeks):
        self.id = id
        self.HoursWorked = 0
        self.distancesBetweenPlacesToWatch = distancesBetweenPlacesToWatch
        self.expectedPlaceToWatch = expectedPlaceToWatch
        self.shiftPreferences = shiftPreferences
        self.shifts = np.zeros(168*numberWeeks)
        self.HoursWeeks = np.zeros(numberWeeks)      

    def isVigilantAvailable(self,startPeriod,endPeriod,maxWorkHoursPerWeek):
        if self.hasEnoughHoursToWorkInThisShift(startPeriod,endPeriod,maxWorkHoursPerWeek) == False:
            return False
        if self.hasEnoughResting(startPeriod) == False:
           return False
        if self.isAvailableInShift(startPeriod,endPeriod) == False:
            return False        
        return self.canWorkThisSunday(startPeriod,endPeriod)
    
    def isAvailableInShift(self,startPeriod,endPeriod):
        for period in range(startPeriod,endPeriod+17):
            if period == len(self.shifts)-1:
                break
            if self.shifts[period] != 0:
                return False
        return True

    def hasEnoughResting(self,period):
        for Actualperiod in range(period-1, period-17,-1):
            if Actualperiod <= 0:
                break
            if self.shifts[Actualperiod] != 0:
                return False
        return True

     #Check restrictions   
    def hasEnoughHoursToWorkInThisShift(self,startPeriod,endPeriod,maxHours):
        weekStarPeriod = math.floor(startPeriod/168)
        weekEndPeriod  =  math.floor(endPeriod/168)
        if weekStarPeriod == weekEndPeriod:
            if  (self.HoursWeeks[weekStarPeriod]+(endPeriod - startPeriod)) <= maxHours:
                return True
            return False
        else:
            if (self.HoursWeeks[weekStarPeriod]+(168*weekEndPeriod)-startPeriod) <= maxHours and (self.HoursWeeks[weekEndPeriod]+endPeriod-(168*weekEndPeriod)) <= maxHours:
                return True
        return False
    
    def canWorkThisSunday(self,startPeriod,endPeriod):
        weekToCheck = math.floor(startPeriod/168)
        if self.thereIsAPeriodInSunday(startPeriod,endPeriod,weekToCheck):
            return self.workLastSunday(weekToCheck)
        return True
    
    def workLastSunday(self,week):
        if week == 0:
            return True
        for period in range (168*week,(168*week)-24,-1):
            if self.shifts[period] != 0:
                return False
        return True
    
    def thereIsAPeriodInSunday(self,startPeriod,endPeriod,week):
        if (startPeriod > 144+ (168*week) and startPeriod < 168*(week+1)):
            return True
        else:
            if (endPeriod > 144+ (168*week)):
              return True
        return False
   
    def setHoursWorked(self,week):
        self.HoursWeeks[week] = self.HoursWeeks[week]+1
        self.HoursWorked+=1
   
    def setShift(self, period, site):
        self.shifts[period] = site
    
    def setShifts(self,shifts,site):
        for period in range(shifts[0],shifts[1]+1):
            self.setShift(period,site)