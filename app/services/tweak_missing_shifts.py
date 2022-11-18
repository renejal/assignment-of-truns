import random
from typing import List, Dict
from dominio.model.shift_place import Shift_place
from dominio.Component import Component
from conf.settings import ACTIVE_CASES,MAXIMUM_WORKING_AMOUNT_HOURS_BY_WEEK,MAXIMUM_EXTRA_WORKING_AMOUNT_HOURS_BY_WEEK,STOP_GRASP_TWEAK
from dominio.Solution import Solution
from dominio.model.shift import Shift
from dominio.model.vigilant import Vigilant
from services.vigilant_assigment_service import Vigilant_assigment_service

class Tweak_missing_shifts:

    vigilant_assigment_service: Vigilant_assigment_service = Vigilant_assigment_service(None)
        
    def missing_shifts_tweak(self, solution: Solution) -> Solution:
        if solution.missing_shifts_fitness == 0:
            return solution
        vigilantes_with_missing_hours: List[Vigilant] = self.get_vigilantes_with_missing_hours(solution.vigilantes_schedule)
        #Asignar a los turnos los vigilantes que tienen menos de 48 horas en el mismo sitio
        case = random.choices([1,2,3,4,5])
        if ACTIVE_CASES and case == 1:
            for site in solution.sites_schedule:
                if len(site.missing_shifts) == 0:
                    continue
                vigilantes = [x for x in vigilantes_with_missing_hours if site.site_id in x.sites_to_look_out]
                assigned_vigilantes = self.assign_vigilantes_on_missing_shifts(vigilantes,site.site_id,site.missing_shifts)
                for v in assigned_vigilantes:
                    if self.vigilant_assigment_service.check_if_vigilant_has_missing_hours(v) == False:
                        vigilantes_with_missing_hours.remove(v)
                if len(assigned_vigilantes) > 1:
                    if STOP_GRASP_TWEAK:
                        return solution
                if site.site_id == len(solution.sites_schedule): 
                    return solution
        if ACTIVE_CASES and case == 2:
            #Asignar horas extras a los vigilantes en el mismo sitio
            for site in solution.sites_schedule:
                if len(site.missing_shifts) == 0:
                    continue
                assigned_vigilantes = self.assign_extra_hours_on_vigilantes(list(site.assigned_Vigilantes.values()), site.site_id, site.missing_shifts)
                if len(assigned_vigilantes) > 1:
                    if STOP_GRASP_TWEAK:
                        return solution
                if site.site_id == len(solution.sites_schedule): 
                    return solution
        if ACTIVE_CASES and  case == 3:
            #Asignar a los turnos los vigilantes que tienen menos de 48 horas en algun otro sitio
            for site in solution.sites_schedule:      
                if len(site.missing_shifts) == 0:
                    continue      
                vigilantes = self.get_vigilantes_from_other_sites( vigilantes_with_missing_hours, site.assigned_Vigilantes)
                assigned_vigilantes = self.assign_vigilantes_on_missing_shifts(vigilantes,site.site_id,site.missing_shifts)
                for v in assigned_vigilantes:
                    if v.id not in site.assigned_Vigilantes:
                        site.assigned_Vigilantes[v.id] = v
                    if self.vigilant_assigment_service.check_if_vigilant_has_missing_hours(v) == False:
                        vigilantes_with_missing_hours.remove(v)
                if len(assigned_vigilantes) > 1:
                    if STOP_GRASP_TWEAK:
                        return solution
                if site.site_id == len(solution.sites_schedule): 
                    return solution
        if ACTIVE_CASES and  case == 4:    
            #Asignar horas extras a los vigilantes en otro sitio
            for site in solution.sites_schedule:
                if len(site.missing_shifts) == 0:
                    continue
                vigilantes = self.get_vigilantes_from_other_sites( solution.vigilantes_schedule, site.assigned_Vigilantes)    
                assigned_vigilantes = self.assign_extra_hours_on_vigilantes(vigilantes, site.site_id, site.missing_shifts)
                for v in assigned_vigilantes:
                    if v.id not in site.assigned_Vigilantes:
                        site.assigned_Vigilantes[v.id] = v
                if len(assigned_vigilantes) > 1:
                    if STOP_GRASP_TWEAK:
                        return solution
                if site.site_id == len(solution.sites_schedule): 
                    return solution
        if case == 5:
            #Modificar turnos en guardias
            self.change_shift(solution.sites_schedule, solution.vigilantes_schedule)
        return solution
    
    def get_vigilantes_with_missing_hours(self, vigilantes: List [Vigilant]) -> List[Vigilant]:
        vigilantes_with_missing_hours: List[Vigilant] = []
        for vigilant in vigilantes:
            for hours_worked_on_week in vigilant.total_hours_worked_by_week:
                if hours_worked_on_week < MAXIMUM_WORKING_AMOUNT_HOURS_BY_WEEK and vigilant not in vigilantes_with_missing_hours:
                    vigilantes_with_missing_hours.append(vigilant)
        return vigilantes_with_missing_hours

    def get_vigilantes_from_other_sites(self, vigilantes: List[Vigilant], assigned_vigilants_on_site: Dict[int,Vigilant] ):
        vigilantes_from_other_sites: List[Vigilant] = []
        for vigilant in vigilantes:
            if vigilant.id not in assigned_vigilants_on_site:  
                vigilantes_from_other_sites.append(vigilant)     
        return vigilantes_from_other_sites

    def assign_extra_hours_on_vigilantes(self, vigilantes:List[Vigilant], site_id: int, shifts: List[Shift]):
        self.vigilant_assigment_service._MAXIMUM_WORKING_AMOUNT_HOURS_BY_WEEK = MAXIMUM_EXTRA_WORKING_AMOUNT_HOURS_BY_WEEK
        assigned_vigilantes =self.assign_vigilantes_on_missing_shifts(vigilantes,site_id, shifts)
        self.vigilant_assigment_service._MAXIMUM_WORKING_AMOUNT_HOURS_BY_WEEK = MAXIMUM_WORKING_AMOUNT_HOURS_BY_WEEK
        return assigned_vigilantes

    def assign_vigilantes_on_missing_shifts(self, vigilantes:List[Vigilant], site_id: int, shifts: List[Shift])-> List[Vigilant] :
        random.shuffle(vigilantes)
        random.shuffle(shifts)
        assigned_vigilantes: List[Vigilant] = []
        assigned_vigilantes_in_actual_shift: List[int] = []
        index = 0
        while index < len(shifts):
            shift = shifts[index]
            assigned_vigilantes_in_actual_shift.clear()
            for iteration in range(shift.necesary_vigilantes - len(shift.assigment_vigilantes)):
                for vigilant in vigilantes:    
                    if vigilant not in assigned_vigilantes_in_actual_shift and self.vigilant_assigment_service.is_vigilant_avaible(vigilant, shift):
                        vigilant.assign_shift(shift, site_id)
                        shift.add_vigilant(vigilant.id)
                        assigned_vigilantes_in_actual_shift.append(vigilant.id)
                        if vigilant not in assigned_vigilantes:
                            assigned_vigilantes.append(vigilant)
                        if self.vigilant_assigment_service.check_if_vigilant_has_missing_hours(vigilant)!= True:
                            vigilantes.remove(vigilant)
                            #Mejorar porque ese repite el proveso
                        break
            if shift.necesary_vigilantes == len(shift.assigment_vigilantes):
                shifts.remove(shift)
                index-=1
            index+=1
        return assigned_vigilantes    

    def change_shift(self,sites: List[Component], vigilantes: List[Vigilant]):
        siteRamdon = random.randrange(0, len(sites)-1)
        siteRamdon2 = random.randrange(0, len(sites)-1)
        site = sites[siteRamdon]
        site2 = sites[siteRamdon2]
        for k in range(100):
            shiftramdon = random.randrange(0, len(site.site_schedule)-1)
            shiftramdon2 = random.randrange(0, len(site2.site_schedule)-1)
            shift = site.site_schedule[shiftramdon]
            shift2 = site2.site_schedule[shiftramdon2]
            for i in shift.assigment_vigilantes:
                vigilant = vigilantes[i-1]
                if vigilant.id not in shift2.assigment_vigilantes and self.vigilant_assigment_service.is_available_on_shift(vigilant,shift2):
                    for j in shift2.assigment_vigilantes:
                        vigilant2 = vigilantes[j-1]
                        if self.vigilant_assigment_service.is_available_on_shift(vigilant2,shift):
                            shiftttt = vigilant.find_shift_place(shift)
                            shiftttt2 = vigilant2.find_shift_place(shift2)
                            self.change_shifts_vigilantes(site,site2,shiftttt,shiftttt2, vigilant, vigilant2 )
                            return
    def change_shifts_vigilantes(self, site1: Component, site2: Component, shift1: Shift_place, shift2: Shift_place, vigilant1: Vigilant, vigilant2: Vigilant) -> None:
        self.change_shift_vigilant(site1, site2, shift1, shift2, vigilant1, vigilant2)
        self.change_shift_vigilant(site2, site1, shift2, shift1, vigilant2, vigilant1)

    def change_shift_vigilant(self,actual_site:Component, site_to_change: Component, actual_shift: Shift_place, shift_to_change: Shift_place, actual_vigilant:Vigilant, vigilant_to_change: Vigilant) -> None:
        actual_vigilant.remove_shift(actual_shift)
        actual_vigilant.assign_shift(shift_to_change.shift,shift_to_change.site_id)
        shift_to_change.shift.change_vigilant(vigilant_to_change.id, actual_vigilant.id)
        if actual_site.site_id not in actual_vigilant.sites_to_look_out:
            actual_site.assigned_Vigilantes.pop(actual_vigilant.id)            
        if actual_vigilant.sites_to_look_out.get(site_to_change.site_id) == 1:
            site_to_change.assigned_Vigilantes[actual_vigilant.id] = actual_vigilant