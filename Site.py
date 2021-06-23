class Site:
    HoursMin = 0
    HoursMax = 0
    HoursMinRest = 0
    HoursMaxRest = 0
    #vigilantesDefault = [ [1,2,3]],[4,5,6],..]
    

    def __int__(self, hoursMin, hoursMax, hourMaxRest, hoursMinRest):
        self.HoursMin = hoursMin
        self.HoursMax = hoursMax
        self.HoursMaxRest = hourMaxRest
        self.HoursMinRest = hoursMinRest



