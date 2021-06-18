from Turno import  Turno
import numpy as np

class Vigilant:

    def __init__(self,id, expectedPlace,preferences,distances,numberWeek):
        self.id = id
        self.shifts = []
        self.HoursWorked = 0
        self.HoursWeeks = []
        self.HoursofRest = 0
        self.preferences = preferences
        self.distances = distances
        self.expectedPlace = expectedPlace
        self.initShift(numberWeek)


    def initShift(self, numberWeek):
        for i in range(numberWeek):
            week = []
            # week = np.zeros(168)
            for j in range(168):
                week.append(Turno())
            self.shifts.append(week)
            self.HoursWeeks.append(0)

    def availabilityShift(self,startPeriod,endPeriod):
        shift =  self.ShiftConvert(startPeriod)
        if endPeriod > 168 * (shift[1]+1):
            changePeriod = 168 - startPeriod
            for period in range(shift[0],shift[0]+changePeriod):
                if self.shifts[shift[1]][period] == 0: #change to different
                    return False
            for period in range(0,endPeriod-startPeriod-changePeriod):
                if self.shifts[shift[1]+1][period] == 0: #change to different
                    return False
            return True
        for period in range(shift[0],endPeriod-startPeriod+shift[0]):
            if self.shifts[shift[1]][period] == 0: #change to different
                return False
        return True
        
    def ShiftConvert(self, shift):
        i = 0
        while shift >= 168:
            shift = shift - 168
            i = i + 1
        return shift, i



