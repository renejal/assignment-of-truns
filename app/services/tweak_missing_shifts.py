from random import shuffle
import random
from typing import List, Dict

from scipy.fftpack import shift
from dominio.Solution import Solution
from dominio.model.shift import Shift
from dominio.model.vigilant import Vigilant
from services.vigilant_assigment_service import Vigilant_assigment_service

class Tweak_missing_shifts:

    vigilant_assigment_service: Vigilant_assigment_service = Vigilant_assigment_service(None)
        
    def missing_shifts_tweak(self, solution: Solution) -> Solution:
        vigilantes_with_missing_hours: List[Vigilant] = self.get_vigilantes_with_missing_hours(solution.vigilantes_schedule)
        #Asignar a los turnos los vigilantes que tienen menos de 40 horas en el mismo sitio
        for site in solution.sites_schedule:
             vigilantes = [x for x in vigilantes_with_missing_hours if site.site_id in x.sites_to_look_out]
             assigned_vigilantes = self.assign_vigilantes_on_missing_shifts(vigilantes,site.site_id,site.missing_shifts)
             for v in assigned_vigilantes:
                 if self.vigilant_assigment_service.check_if_vigilant_has_missing_hours(v) == False:
                     vigilantes_with_missing_hours.remove(v)
        #Asignar horas extras a los vigilantes en el mismo sitio
        for site in solution.sites_schedule:
            self.assign_extra_hours_on_vigilantes(list(site.assigned_Vigilantes.values()), site.site_id, site.missing_shifts)
        #Asignar a los turnos los vigilantes que tienen menos de 40 horas en algun otro sitio
        for site in solution.sites_schedule:            
            vigilantes = self.get_vigilantes_from_other_sites( vigilantes_with_missing_hours, site.assigned_Vigilantes)
            assigned_vigilantes = self.assign_vigilantes_on_missing_shifts(vigilantes,site.site_id,site.missing_shifts)
            for v in assigned_vigilantes:
                if v.id not in site.assigned_Vigilantes:
                    site.assigned_Vigilantes[v.id] = v
                if self.vigilant_assigment_service.check_if_vigilant_has_missing_hours(v) == False:
                     vigilantes_with_missing_hours.remove(v)
        #Asignar horas extras a los vigilantes en otro sitio
        for site in solution.sites_schedule:
            vigilantes = self.get_vigilantes_from_other_sites( solution.vigilantes_schedule, site.assigned_Vigilantes)    
            assigned_vigilantes = self.assign_extra_hours_on_vigilantes(vigilantes, site.site_id, site.missing_shifts)
            for v in assigned_vigilantes:
                if v.id not in site.assigned_Vigilantes:
                    site.assigned_Vigilantes[v.id] = v
        #Modificar turnos en guardias
        return solution

    def get_vigilantes_with_missing_hours(self, vigilantes: List [Vigilant]) -> List[Vigilant]:
        vigilantes_with_missing_hours: List[Vigilant] = []
        for vigilant in vigilantes:
            for hours_worked_on_week in vigilant.total_hours_worked_by_week:
                if hours_worked_on_week < 40 and vigilant not in vigilantes_with_missing_hours:
                    vigilantes_with_missing_hours.append(vigilant)
        return vigilantes_with_missing_hours

    def get_vigilantes_from_other_sites(self, vigilantes: List[Vigilant], assigned_vigilants_on_site: Dict[int,Vigilant] ):
        vigilantes_from_other_sites: List[Vigilant] = []
        for vigilant in vigilantes:
            if vigilant.id not in assigned_vigilants_on_site:  
                vigilantes_from_other_sites.append(vigilant)     
        return vigilantes_from_other_sites

    def assign_extra_hours_on_vigilantes(self, vigilantes:List[Vigilant], site_id: int, shifts: List[Shift]):
        self.vigilant_assigment_service._MAXIMUM_WORKING_AMOUNT_HOURS_BY_WEEK = 56
        assigned_vigilantes =self.assign_vigilantes_on_missing_shifts(vigilantes,site_id, shifts)
        self.vigilant_assigment_service._MAXIMUM_WORKING_AMOUNT_HOURS_BY_WEEK = 48
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
