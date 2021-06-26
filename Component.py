class Component:    
    def __init__(self,solution,siteId,cantWeeks,vigilantsByPeriod):   
        self.solution = solution
        self.siteId = siteId
        self.siteSchedule = [[]] * 168*cantWeeks
        self.newVigilants = []
        self.vigilantsByPeriod = vigilantsByPeriod
        self.fitness = 0

    def calcuteFitness(self):
        #Calculate missing shifts
        for period in len(self.siteSchedule):
            self.fitnes += (self.vigilantsByPeriod[period] - len(self.siteSchedule[period]))*100
        #Calculate distances
        for vigilant in self.newVigilants:
            for assignedPlace in vigilant.shifts:
                if assignedPlace != 0:
                    self.fitnes+= vigilant.expectedPlace - assignedPlace
        
