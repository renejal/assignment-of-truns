from typing import List
from dominio.Component import Component
from dominio.model.vigilant import Vigilant
from dominio.model.shift import Shift
import random
from services.vigilant_assigment_service import Vigilant_assigment_service

class site_schedule_service:
    
    def get_site_schedule(self,site_id: int, shifts: List[Shift] , possible_vigilantes_to_assign_ordered_by_criteria: List[List[Vigilant]]) -> Component: 
        assigned_vigilantes_in_actual_shift: List[Vigilant] = []
        assigned_vigilantes: List[Vigilant] = []
        for shift in shifts:
            assigned_vigilantes_in_actual_shift.clear()
            for iteration in range(0, shift.necesary_vigilantes):
                vigilant = self.get_vigilant_avaiable(shift, assigned_vigilantes_in_actual_shift, possible_vigilantes_to_assign_ordered_by_criteria)
                if vigilant != None:
                    vigilant.assign_shift(shift)
                    shift.add_vigilant(vigilant)
                    assigned_vigilantes_in_actual_shift.append(vigilant)
                    if vigilant not in assigned_vigilantes:
                        assigned_vigilantes.append(vigilant)
        return Component(site_id,shifts,assigned_vigilantes)
            

    @staticmethod    
    def get_vigilant_avaiable(shift: Shift, assigned_vigilants_in_actual_shift, possible_vigilantes_to_assign_ordered_by_criteria: List[List[Vigilant]]):
        for vigilantes in possible_vigilantes_to_assign_ordered_by_criteria:
            index_vigilantes = [*range(len(vigilantes))]
            while index_vigilantes:
                index_vigilant = random.choice(index_vigilantes)
                possible_vigilant_to_assing = vigilantes[index_vigilant]
                if possible_vigilant_to_assing not in assigned_vigilants_in_actual_shift and Vigilant_assigment_service.is_vigilant_avaible(possible_vigilant_to_assing, shift):
                    possible_vigilant_to_assing = possible_vigilant_to_assing
                    return possible_vigilant_to_assing
                index_vigilantes.remove(index_vigilant)
        return None

   
