class Site:
    HoursMin = 0
    HoursMax = 0
    HoursMinRest = 0
    HoursMaxRest = 0
    vigilantesDefault = []

    def __int__(self, hoursMin, hoursMax, hourMaxRest, hoursMinRest):
        self.HoursMin = hoursMin
        self.HoursMax = hoursMax
        self.HoursMaxRest = hourMaxRest
        self.HoursMinRest = hoursMinRest



