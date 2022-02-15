from xml.dom import ValidationErr
from dominio.model.shift import Shift
from conf.settings import DISTANCE_FITNESS_VALUE, ASSIGNED_VIGILANTES_FITNESS_VALUE, EXTRA_HOURS_FITNESS_VALUE, MISSING_FITNESS_VALUE
from typing import List
from dominio.model.vigilant import Vigilant

class Component:

    site_id: int
    site_schedule: List[Shift]
    missing_shifts: List[Shift]
    assigned_Vigilantes: List[Vigilant] #No usar para futuras operaciones ya que este queda desactulizado, a medida de cada sitio, usar el vigilante de la solucion mejor
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
 
    def get_vigilantes(self) -> List[Vigilant]:
        return self.assigned_Vigilantes
    
    def get_vigilant(self, id: int)-> Vigilant:
        for vigilant in self.assigned_Vigilantes:
            if vigilant.id == id:
                return vigilant 
             
                
                

    def calculate_inicial_fitness(self) -> None:
        for shift in self.site_schedule:
            if shift.necesary_vigilantes != len(shift.assigment_vigilantes):
                self.missing_shifts.append(shift)
                self.missing_shifts_fitness+= MISSING_FITNESS_VALUE*(shift.necesary_vigilantes - len(shift.assigment_vigilantes))
                self.total_fitness+= MISSING_FITNESS_VALUE*(shift.necesary_vigilantes - len(shift.assigment_vigilantes))  
        if self.assigned_Vigilantes == None:
            return
        for vigilant in self.assigned_Vigilantes:
            if vigilant.default_place_to_look_out !=1 and vigilant.default_place_to_look_out != self.site_id and vigilant.closet_place != self.site_id:
                self.distance_fitness+= DISTANCE_FITNESS_VALUE
                self.total_fitness+= DISTANCE_FITNESS_VALUE  
            #TODO Revisar si es mejor calcular las horas por semaana si trabajo o algo
            for index,hour_by_week in enumerate(vigilant.total_hours_worked_by_week):
                # if index-1 == len(vigilant.total_hours_worked_by_week):
                #     break
                if hour_by_week > 48:
                    self.extra_hours_fitness += EXTRA_HOURS_FITNESS_VALUE
                    self.total_fitness += EXTRA_HOURS_FITNESS_VALUE
                if hour_by_week < 40 and hour_by_week > 0:
                    self.assigned_vigilantes_fitness += ASSIGNED_VIGILANTES_FITNESS_VALUE
                    self.total_fitness+= ASSIGNED_VIGILANTES_FITNESS_VALUE
