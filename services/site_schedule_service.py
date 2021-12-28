from typing import List
from dominio.Component import Component
from dominio.model.vigilant import Vigilant
from dominio.model.shift import Shift
import random
from dominio.vigilant_assigment import VigilantAssigment
from services.vigilant_assigment_service import Vigilant_assigment_service

class site_schedule_service:

    def get_site_schedule(self,site_id: int, shifts: List[Shift], vigilantes: List[Vigilant]) -> Component: 
        assigned_vigilantes_in_actual_shift: List[Vigilant] = []
        assigned_vigilantes: List[Vigilant] = Vigilant_assigment_service.obtain_vigilants_in_default_for_site(site_id)
        for shift in shifts:
            assigned_vigilantes_in_actual_shift.clear()
            for iteration in range(0, shift.necesary_vigilantes):
                vigilant: Vigilant = self.get_vigilant_avaiable(site_id ,shift, assigned_vigilantes_in_actual_shift , assigned_vigilantes , vigilantes)
                if vigilant != None:
                    vigilant.assign_shift(shift)
                    shift.add_vigilant(vigilant.id)
                    assigned_vigilantes_in_actual_shift.append(vigilant)
                    if vigilant not in assigned_vigilantes:
                        assigned_vigilantes.append(vigilant)
        return Component(site_id,shifts,assigned_vigilantes)
            

    @staticmethod    
    def get_vigilant_avaiable(site_id: int, shift: Shift, assigned_vigilants_in_actual_shift, vigilantes) -> Vigilant:
        
        Vigilant_assigment_service.get_possible_vigilant_to_assign( )
        
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

   
