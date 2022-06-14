from pickle import FALSE
from xml.dom import ValidationErr
from dominio.model.shift import Shift
from conf.settings import DISTANCE_FITNESS_VALUE, ASSIGNED_VIGILANTES_FITNESS_VALUE, EXTRA_HOURS_FITNESS_VALUE, MISSING_FITNESS_VALUE
from typing import List, Dict
from dominio.model.vigilant import Vigilant

class Component:

    site_id: int
    site_schedule: List[Shift]
    missing_shifts: List[Shift]
    assigned_Vigilantes: Dict[int,Vigilant] 
    
    missing_shifts_fitness: int = 0
    distance_fitness: int = 0
    extra_hours_fitness: int = 0
    assigned_vigilantes_fitness: int = 0
    modified = False
    total_fitness:int = 0
    
    def __init__(self, site_id : int , site_schedule : List[Shift], assigned_vigilantes: List[Vigilant]) -> None:   
        self.site_id = site_id
        self.site_schedule = site_schedule
        self.assigned_Vigilantes = {x.id: x for x in assigned_vigilantes}
        self.missing_shifts = []
        self.calculate_inicial_fitness()
 
    def get_vigilantes(self) -> List[Vigilant]:
        return self.assigned_Vigilantes
    
    def get_vigilant(self, id: int)-> Vigilant:
        for vigilant in self.assigned_Vigilantes:
            if vigilant == id:
                return self.assigned_Vigilantes.get(id) 
    def set_remove_vigilant(self, vigilants: List[int]):
        for vigilant in self.assigned_Vigilantes:
            if vigilant.id in vigilants:
                self.assigned_Vigilantes.remove(vigilant)
    def exchange_vigilant(self, id_vigilant_new, id_vigilant_exchange):
        self.get_vigilant(id_vigilant_exchange).set_id(id_vigilant_new)

    def calculate_inicial_fitness(self) -> None:
        for shift in self.site_schedule:
            if shift.necesary_vigilantes != len(shift.assigment_vigilantes):
                self.missing_shifts.append(shift)
                self.missing_shifts_fitness+= MISSING_FITNESS_VALUE*(shift.necesary_vigilantes - len(shift.assigment_vigilantes))
                self.total_fitness+= MISSING_FITNESS_VALUE*(shift.necesary_vigilantes - len(shift.assigment_vigilantes))  
        if self.assigned_Vigilantes == None:
            return
        for vigilant in self.assigned_Vigilantes.values():
            if vigilant.default_place_to_look_out !=1 and vigilant.default_place_to_look_out != self.site_id and vigilant.closet_place != self.site_id:
                # self.distance_fitness+= vigilant.distances[self.site_id-1]
                # self.total_fitness+= vigilant.distances[self.site_id-1]  
                self.distance_fitness+= DISTANCE_FITNESS_VALUE * vigilant.order_distances.get(self.site_id)
                self.total_fitness+= DISTANCE_FITNESS_VALUE * vigilant.order_distances.get(self.site_id) 
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

    def get_fitness_by_criteria(self, fitnessToOptimize:str) -> int:
        if fitnessToOptimize == "missing_shifts":
            return self.missing_shifts_fitness
        if fitnessToOptimize == "necesary_vigilantes":
            return self.assigned_vigilantes_fitness
        if fitnessToOptimize == "extra_hours":
            return self.extra_hours_fitness
        if fitnessToOptimize == "distance":
            return self.distance_fitness

    def order_workings_days(self):
        "ordenamiento por seleccios"
        for i in range(len(self.site_schedule)):
            temp = i
            for j in range(i+1, len(self.site_schedule)):
                if self.site_schedule[j].shift_start < self.site_schedule[temp].shift_start:
                    temp = j
            self.site_schedule[i], self.site_schedule[temp] = self.site_schedule[temp], self.site_schedule[i]
        
        self.assigment_id_order()
    def assigment_id_order(self):
        pass

            
            



        


            
