import numpy as np
import math
class Vigilant:

    def __init__(self,id, expectedPlaceToWatch,shiftPreferences,distancesBetweenPlacesToWatch,numberWeeks):
        self.id = id
        self.HoursofRest = 0
        self.HoursWorked = 0
        self.distancesBetweenPlacesToWatch = distancesBetweenPlacesToWatch
        self.expectedPlaceToWatch = expectedPlaceToWatch
        self.shiftPreferences = shiftPreferences
        self.shifts = np.zeros(168*numberWeeks)
        self.HoursWeeks = np.zeros(numberWeeks)      

    def isVigilantAvailable(self,startPeriod,endPeriod):
        if self.hasEnoughHoursToWorkInThisShift(startPeriod,endPeriod) == False:
            return False
        if self.isAvailableInShift(startPeriod,endPeriod) == False:
            return False
        if self.hasEnoughResting(startPeriod) == False:
           return False
        #return self.canWorkThisSunday(startPeriod,endPeriod)
        return True
    
    def isAvailableInShift(self,startPeriod,endPeriod):
        for period in range(startPeriod,endPeriod):
            if self.shifts[period] != 0:
                return False
        return True

    def hasEnoughResting(self,period):
        for period in range(period, period-16,-1):
            if period == 0:
                break
            if self.shifts[period] != 0:
                return False
        return True
        
    def hasEnoughHoursToWorkInThisShift(self,startPeriod,endPeriod):
        weekStarPeriod = math.floor(startPeriod/168)
        weekEndPeriod  =  math.floor(endPeriod/168)
        if weekStarPeriod == weekEndPeriod:
            if  (self.HoursWeeks[weekStarPeriod]+(endPeriod - startPeriod)) <= 56:
                for period in range(startPeriod, startPeriod+16):
                    if period == len(self.shifts)-1:
                        break
                    if self.shifts[period] != 0:
                        return False
                return True
            return False
        else:
            if (self.HoursWeeks[weekStarPeriod]+(168*weekEndPeriod)-startPeriod) <= 56 and (self.HoursWeeks[weekEndPeriod]+endPeriod-(168*weekEndPeriod)) <= 56:
                for period in range(startPeriod, startPeriod+16):
                    if period == len(self.shifts)-1:
                        break
                    if self.shifts[period] != 0:
                        return False
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
    
    def thereIsAPeriodInSunday(startPeriod,endPeriod,week):
        if (startPeriod > 144+ (168*week) and startPeriod < 168*(week+1)):
            return True
        else:
            if (endPeriod > 144+ (168*week)):
              return True
        return False
   
    def setHoursWorked(self,week):
        self.HoursWeeks[week] = self.HoursWeeks[week]+1
    
    def setHoursRest(self, hours):
        self.HoursofRest = self.HoursofRest + hours
   
    def setShift(self, period, site):
        self.shifts[period] = site