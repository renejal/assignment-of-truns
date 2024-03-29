from typing import List
from conf.settings import WINDOWS_RANDOM_THE_VIGILANTS_ORDER_FOR_SITE, SHUFFLE
from dominio.Component import Component
from dominio.model.vigilant import Vigilant
from dominio.model.shift import Shift
import random
from dominio.vigilant_assigment import VigilantAssigment
from services.vigilant_assigment_service import Vigilant_assigment_service

class Site_schedule_service:

    vigilant_assigment_service: Vigilant_assigment_service

    def __init__(self, problem: VigilantAssigment):
        self.vigilant_assigment_service = Vigilant_assigment_service(problem)

    def get_site_schedule(self,site_id: int, shifts: List[Shift], order_vigilantes: List[Vigilant], expected_vigilantes_in_place: List[Vigilant]) -> Component: 
        assigned_vigilantes_in_actual_shift: List[int] = []
        assigned_vigilantes_on_place: List[Vigilant] = expected_vigilantes_in_place
        self.shuffle_first_shifts(shifts)
        for shift in shifts:
            assigned_vigilantes_in_actual_shift.clear()
            for iteration in range(shift.necesary_vigilantes):
                vigilant_to_assign: Vigilant = self.get_vigilant_avaiable(shift, order_vigilantes, assigned_vigilantes_in_actual_shift , assigned_vigilantes_on_place , site_id)
                if vigilant_to_assign != None:
                    self.assign_vigilant(site_id,shift,vigilant_to_assign, assigned_vigilantes_on_place)
                    assigned_vigilantes_in_actual_shift.append(vigilant_to_assign.id)    
                else:
                    break                
        return Component(site_id,shifts,assigned_vigilantes_on_place)
    
    def get_vigilant_avaiable(self, shift: Shift, order_vigilantes : List[Vigilant], assigned_vigilants_in_actual_shift: List[int], 
                              assigned_vigilantes_on_place: List[Vigilant], site_id : int) -> Vigilant:                               
        vigilant_to_assign = self.get_vigilant_available_on_list(assigned_vigilantes_on_place, assigned_vigilants_in_actual_shift, shift , site_id)
        if vigilant_to_assign != None:
            return vigilant_to_assign
        start_index_to_select_vigilantes = 0
        while start_index_to_select_vigilantes < len(order_vigilantes):
            possible_vigilantes_to_assign = order_vigilantes[start_index_to_select_vigilantes:start_index_to_select_vigilantes + WINDOWS_RANDOM_THE_VIGILANTS_ORDER_FOR_SITE]
            vigilant_to_assign = self.get_vigilant_available_on_list(possible_vigilantes_to_assign , assigned_vigilants_in_actual_shift, shift , site_id)
            if vigilant_to_assign != None:
                return vigilant_to_assign
            start_index_to_select_vigilantes+= WINDOWS_RANDOM_THE_VIGILANTS_ORDER_FOR_SITE
        return None
    
    def get_vigilant_available_on_list(self, vigilantes: List[Vigilant], assigned_vigilants_in_actual_shift:List[int], shift: Shift , site_id: int) -> Vigilant:
        if not vigilantes:
            return None
        random.shuffle(vigilantes)
        for possible_vigilant_to_assing in vigilantes:
            if possible_vigilant_to_assing.id not in assigned_vigilants_in_actual_shift and (possible_vigilant_to_assing.default_place_to_look_out == site_id or possible_vigilant_to_assing.default_place_to_look_out == -1):
                if self.vigilant_assigment_service.is_vigilant_avaible(possible_vigilant_to_assing, shift):
                    return possible_vigilant_to_assing
        return None

    def assign_vigilant(self, site_id:int, shift: Shift, vigilant_to_assign: Vigilant, assigned_vigilantes_on_place: List[Vigilant]):
        if vigilant_to_assign not in assigned_vigilantes_on_place:
            assigned_vigilantes_on_place.append(vigilant_to_assign)
        vigilant_to_assign.assign_shift(shift, site_id)
        shift.add_vigilant(vigilant_to_assign.id)
   
    def shuffle_first_shifts(self, shifts:List[Shift]):
        if SHUFFLE:
            shuffle_first_shifts = shifts[:9]
            random.shuffle(shuffle_first_shifts)
            shifts[:9] = shuffle_first_shifts
