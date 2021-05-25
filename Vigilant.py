from Turno import  Turno
class Vigilant:

    def __init__(self, numberWeek):
        self.shifts = []
        self.HoursWorked = 0
        self.HoursWeeks = []
        self.HoursofRest = 0
        self.initShift(numberWeek)


    def initShift(self, numberWeek):
        for i in range(numberWeek):
            week = []
            for j in range(168):
                week.append(Turno())
            self.shifts.append(week)





