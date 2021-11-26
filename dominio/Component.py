from dominio.Shift import Shift
from typing import List

from dominio.Vigilant3 import Vigilant

class Component:

    __site_id: int
    __site_schedule: List[Shift]
    __missing_shifts: List[Shift]
    __assigned_Vigilants: List[Vigilant]
    
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

    def calculateFitness2(self) -> None:
        for shift in self.__site_schedule:
            if shift.__necesary_vigilants != len(shift.__assigment_vigilants):
                self.__missing_shifts.append(shift)
                self.__missing_shifts_fitness+= 1000   
        for vigilant in self.__assigned_Vigilants:
            if vigilant.__expected_place_to_work !=0 and vigilant.__expected_place_to_work != self.__site_id:
                self.__distance_fitness+= 500
            for hour_week in vigilant.__hours_worked_by_week:
                if hour_week > 48 :
                    self.__extra_hours_fitness+= 200 * (hour_week- 48)
                    
##Verificar si __assigned_vigilants_fitness tocaria incluirlo aqui.
