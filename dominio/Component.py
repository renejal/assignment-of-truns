from dominio.Shift import Shift
from typing import List

class Component:

    __site_id: int
    __site_schedule: List[Shift]
    __missing_shifts: List[Shift]
    __missing_shifts_fitness: int
    __distance_fitness: int
    __extra_hours_fitness: int
    __assigned_vigilants_fitness: int

    def __init__(self, site_id : int , site_schedule : List[Shift]) -> None:   
        self.__site_id = site_id
        self.__site_schedule = site_schedule

    def calcuteFitness(self) -> None: #decraped
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
                    
