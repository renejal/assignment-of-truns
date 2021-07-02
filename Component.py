class Component:    
    def __init__(self,solution,siteId,cantWeeks,vigilantsByPeriod):   
        self.solution = solution
        self.siteId = siteId
        self.siteSchedule = []
        for i in range(0,168*cantWeeks):
            self.siteSchedule.append([])
        self.newVigilants = []
        self.vigilantsByPeriod = vigilantsByPeriod
        self.fitness = 0

    def calcuteFitness(self):
        #Calculate missing shifts
        for period in range(0,len(self.siteSchedule)):
            self.fitness += (self.vigilantsByPeriod[period] - len(self.siteSchedule[period]))*100
        #Calculate distances
        for vigilant in self.newVigilants:
            for assignedPlace in vigilant.shifts:
                if assignedPlace != 0:
                    self.fitnes+= vigilant.expectedPlace - assignedPlace
        
