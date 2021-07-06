class Component:    
    def __init__(self,siteId,cantWeeks,necesaryvigilantsByPeriod):   
        self.siteId = siteId
        self.siteSchedule = []
        for period in range(0,168*cantWeeks):
            self.siteSchedule.append([])
        self.assignedVigilants = []
        self.necesaryvigilantsByPeriod = necesaryvigilantsByPeriod
        self.fitness = 0

    def calcuteFitness(self):
        #Calculate missing shifts
        for period in range(0,len(self.siteSchedule)):
            self.fitness += (self.necesaryvigilantsByPeriod[period] - len(self.siteSchedule[period]))*100
        #Calculate distances and preferences
        for vigilant in self.assignedVigilants:
            for assignedPlace in vigilant.shifts:
                if assignedPlace != 0:
                    #calculate fitness distance
                    self.fitnes+= vigilant.expectedPlace - assignedPlace
                    #Calculate preferencias 
                    #TODO 
                    
