from dominio.model.shift import Shift
from typing import List

from dominio.model.vigilant import Vigilant

class Component:

    site_id: int
    site_schedule: List[Shift]
    missing_shifts: List[Shift]
    assigned_Vigilantes: List[Vigilant]
    
    missing_shifts_fitness: int = 0
    distance_fitness: int = 0
    extra_hours_fitness: int = 0
    assigned_vigilantes_fitness: int = 0
    total_fitness:int = 0
    
    def __init__(self, site_id : int , site_schedule : List[Shift], assigned_vigilantes: List[Vigilant]) -> None:   
        self.site_id = site_id
        self.site_schedule = site_schedule
        self.assigned_Vigilantes = assigned_vigilantes
        self.missing_shifts = []
        self.calculate_inicial_fitness()

    def calculate_fitness(self) -> None: #decraped
        #Calculate missing shifts
        for period in range(0,len(self.siteSchedule)):
            missingVigilantes = self.necesaryvigilantesByPeriod[period] - len(self.siteSchedule[period])
            if(missingVigilantes != 0):
                self.missingShfits.append(period)
            self.fitness += missingVigilantes*10000
        #Calculate distances and preferences
        for vigilant in self.assignedVigilantes:
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

    def calculate_inicial_fitness(self) -> None:
        for shift in self.site_schedule:
            if shift.necesary_vigilantes != len(shift.assigment_vigilantes):
                self.missing_shifts.append(shift)
                self.missing_shifts_fitness+= 1000
                self.total_fitness+= 1000  
        if self.assigned_Vigilantes == None:
            return
        for vigilant in self.assigned_Vigilantes:
            if vigilant.default_place_to_look_out !=1 and vigilant.default_place_to_look_out != self.site_id and vigilant.closet_place != self.site_id:
                self.distance_fitness+= 500
                self.total_fitness+= 500  
            for hour_by_week in vigilant.total_hours_worked_by_week:
                if hour_by_week < 40:
                    self.assigned_vigilantes_fitness += 300
                    self.total_fitness+= 300  

