class Component:    
    def __init__(self,siteId,cantWeeks,necesaryvigilantsByPeriod):   
        self.siteId = siteId
        self.siteSchedule = []
        for period in range(0,168*cantWeeks):
            self.siteSchedule.append([])
        self.assignedVigilants = []
        self.necesaryvigilantsByPeriod = necesaryvigilantsByPeriod
        self.fitness = 0
        self.missingShfits = []
        
    def calcuteFitness(self):
        #Calculate missing shifts
        for period in range(0,len(self.siteSchedule)):
            missingVigilants = self.necesaryvigilantsByPeriod[period] - len(self.siteSchedule[period])
            if(missingVigilants != 0):
                self.missingShfits.append(period)
            self.fitness += missingVigilants*10000
        #Calculate distances and preferences
        for vigilant in self.assignedVigilants:
            for assignedPlace in vigilant.shifts:
                if assignedPlace != 0:
                    #calculate fitness distance
                    if vigilant.expectedPlaceToWatch != assignedPlace:
                        self.fitness+= 500
                    #calculate work hours
                    for hourWeek in vigilant.HoursWeeks:
                        if hourWeek < 40 and hourWeek!=0:
                            self.fitness+= 800
                    #Calculate preferencias 
                    #TODO 
                    
