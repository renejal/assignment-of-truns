from typing import List
from conf.settings import WINDOWS_RANDOM_THE_VIGILANTS_ORDER_FOR_SITE
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

    def get_site_schedule(self,site_id: int, shifts: List[Shift], vigilantes: List[Vigilant]) -> Component: 
        assigned_vigilantes_on_place: List[Vigilant] = self.vigilant_assigment_service.obtain_vigilants_in_default_for_site(site_id, vigilantes)
        assigned_vigilantes_in_actual_shift: List[int] = []
        order_vigilantes_index_in_place_by_distance: List[int] = self.vigilant_assigment_service.get_order_vigilantes_index_in_place_by_distance(site_id)
        for shift in shifts:
            assigned_vigilantes_in_actual_shift.clear()
            for iteration in range(0, shift.necesary_vigilantes):
                vigilant_to_assign: Vigilant = self.get_vigilant_avaiable(shift, vigilantes, assigned_vigilantes_in_actual_shift , assigned_vigilantes_on_place , order_vigilantes_index_in_place_by_distance)
                if vigilant_to_assign != None:
                    vigilant_to_assign.assign_shift(shift)
                    shift.add_vigilant(vigilant_to_assign.id)
                    assigned_vigilantes_in_actual_shift.append(vigilant_to_assign.id)
                    if vigilant_to_assign not in assigned_vigilantes_on_place:
                        assigned_vigilantes_on_place.append(vigilant_to_assign)
        return Component(site_id,shifts,assigned_vigilantes_on_place)
            
    def get_vigilant_avaiable(self, shift: Shift, vigilantes : List[Vigilant], assigned_vigilants_in_actual_shift: List[int], assigned_vigilantes_on_place: List[Vigilant], order_vigilantes_index_in_place_by_distance: List[int]) -> Vigilant:                               
        vigilant_to_assign = self.get_vigilant_available_on_list(assigned_vigilantes_on_place, assigned_vigilants_in_actual_shift, shift)
        if vigilant_to_assign != None:
            return vigilant_to_assign
        start_index_to_select_vigilantes = 0
        while start_index_to_select_vigilantes < len(vigilantes):
            possible_vigilantes_to_assign = self.vigilant_assigment_service.get_possible_vigilant_to_assign_by_distance(vigilantes, order_vigilantes_index_in_place_by_distance, start_index_to_select_vigilantes , start_index_to_select_vigilantes + WINDOWS_RANDOM_THE_VIGILANTS_ORDER_FOR_SITE )
            vigilant_to_assign = self.get_vigilant_available_on_list(possible_vigilantes_to_assign , assigned_vigilants_in_actual_shift, shift)
            if vigilant_to_assign != None:
                return vigilant_to_assign
            start_index_to_select_vigilantes+= WINDOWS_RANDOM_THE_VIGILANTS_ORDER_FOR_SITE + 1
        return None
    
    def get_vigilant_available_on_list(self, vigilantes: List[Vigilant], assigned_vigilants_in_actual_shift:List[int], shift: Shift) -> Vigilant:
        index_vigilantes = [*range(len(vigilantes))]
        while index_vigilantes:
            index_vigilant = random.choice(index_vigilantes)
            possible_vigilant_to_assing = vigilantes[index_vigilant]
            if possible_vigilant_to_assing.id not in assigned_vigilants_in_actual_shift and self.vigilant_assigment_service.is_vigilant_avaible(possible_vigilant_to_assing, shift):
                return possible_vigilant_to_assing
            index_vigilantes.remove(index_vigilant)
        return None

   
