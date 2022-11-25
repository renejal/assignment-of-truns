import random
from typing import List

import numpy as np
from conf import settings
from conf.settings import ACTIVE_CASES,MAXIMUM_WORKING_AMOUNT_HOURS_BY_WEEK,MAXIMUM_EXTRA_WORKING_AMOUNT_HOURS_BY_WEEK,STOP_GRASP_TWEAK
from dominio.Solution import Solution
from dominio.model.shift_place import Shift_place
from dominio.model.vigilant import Vigilant
from services.vigilant_assigment_service import Vigilant_assigment_service


class Tweak_assignment_vigilantes_amount:
    vigilant_assigment_service = Vigilant_assigment_service(None)

    def assignment_vigilantes_amount(self, solution: Solution) -> Solution:
        #Obtener vigilantes que tienen menos de 48 horas
        extra_vigilantes_by_week: List[List[Vigilant]] = self.get_extra_vigilantes_by_week(solution.vigilantes_schedule)
        available_vigilantes: List[List[Vigilant]] = self.get_available_vigilantes_by_week(solution.vigilantes_schedule)
        for index_week, extra_vigilantes_on_week in enumerate(extra_vigilantes_by_week):
            random.shuffle(extra_vigilantes_on_week)
            index_vigilant = 0
            while index_vigilant < len(extra_vigilantes_on_week):
                extra_vigilant = extra_vigilantes_on_week[index_vigilant]
                #Si tiene mas de 24 horas trabajas se le quitan las horas a otro vigilante que tenga mas de 48 horas y se las asigna al vigilante que no cumple con las horas minimas
                if extra_vigilant.total_hours_worked_by_week[index_week] > MAXIMUM_WORKING_AMOUNT_HOURS_BY_WEEK / 2:
                    random.shuffle(available_vigilantes[index_week])
                    case = random.choices([1,2])
                    if self.assing_shifts_between_vigilantes_with_extra_hours_and_greater_than_24(extra_vigilant,available_vigilantes[index_week],solution,index_week):
                        extra_vigilantes_on_week.remove(extra_vigilant)
                        index_vigilant-=1
                        if STOP_GRASP_TWEAK:
                            return solution
                    else:
                        vigilants_deleted = self.assing_shifts_between_extra_vigilantes_greater_than(extra_vigilant, extra_vigilantes_by_week , index_week, available_vigilantes, solution)
                        index_vigilant -= vigilants_deleted
                        if vigilants_deleted > 0:
                            if STOP_GRASP_TWEAK:
                                return solution
                #Primero se las asigna a algun otro de los que tienen menos
                #Si tiene menos de 24 horas trabajadas estas horas se las asigna a cualquier otro vigilante que este disponible
                else:
                    shifts = extra_vigilant.get_shifts_on_week(index_week+1)
                    random.shuffle(shifts)
                    for shift_place in shifts:
                        # # random.shuffle(extra_vigilantes_by_week[index_week])
                        var_shift = False
                        index_other_vigilant = 0
                        case = random.choices([1,2])
                        if True:
                            while index_other_vigilant < len(extra_vigilantes_by_week[index_week]):
                                other_extra_vigilant = extra_vigilantes_by_week[index_week][index_other_vigilant]
                                if other_extra_vigilant.id == extra_vigilant.id:
                                    index_other_vigilant+=1
                                    continue
                                if self.vigilant_assigment_service.is_vigilant_avaible_tweaks(other_extra_vigilant, shift_place.shift):
                                    self.exchange_shift(shift_place,extra_vigilant,other_extra_vigilant)
                                    var_shift = True
                                    if other_extra_vigilant.id not in solution.sites_schedule[shift_place.site_id-1].assigned_Vigilantes:
                                        solution.sites_schedule[shift_place.site_id-1].assigned_Vigilantes[other_extra_vigilant.id] = other_extra_vigilant
                                    if shift_place.site_id not in extra_vigilant.sites_to_look_out:
                                        solution.sites_schedule[shift_place.site_id-1].assigned_Vigilantes.pop(extra_vigilant.id)

                                    if other_extra_vigilant.total_hours_worked_by_week[index_week] >= MAXIMUM_WORKING_AMOUNT_HOURS_BY_WEEK:
                                        index_delete = extra_vigilantes_by_week[index_week].index(other_extra_vigilant)
                                        index_actual = extra_vigilantes_by_week[index_week].index(extra_vigilant)
                                        extra_vigilantes_by_week[index_week].remove(other_extra_vigilant)
                                        if index_actual >= index_delete:
                                            index_other_vigilant=-1
                                            index_vigilant-=1
                                            index_actual-=1
                                        available_vigilantes[index_week].append(other_extra_vigilant)

                                    if extra_vigilant.total_hours_worked_by_week[index_week] == 0:
                                        if other_extra_vigilant not in extra_vigilantes_by_week[index_week]:
                                            index_actual = index_delete
                                            index_delete = extra_vigilantes_by_week[index_week].index(extra_vigilant)
                                        else:
                                            index_actual = extra_vigilantes_by_week[index_week].index(other_extra_vigilant)
                                            index_delete = extra_vigilantes_by_week[index_week].index(extra_vigilant)
                                        extra_vigilantes_by_week[index_week].remove(extra_vigilant)
                                        if index_actual >= index_delete:
                                            index_other_vigilant=-1
                                        index_vigilant-=1
                                    if STOP_GRASP_TWEAK:
                                        return solution
                                    break
                                index_other_vigilant+=1
                            if var_shift:
                                if extra_vigilant.total_hours_worked_by_week[index_week] == 0:
                                    if STOP_GRASP_TWEAK:
                                        return solution
                                    break
                                continue
                        random.shuffle(available_vigilantes[index_week])
                        index_available_vigilant = 0
                        while index_available_vigilant < len(available_vigilantes[index_week]):
                            available_vigilant = available_vigilantes[index_week][index_available_vigilant]
                            if self.vigilant_assigment_service.is_vigilant_avaible_tweaks(available_vigilant, shift_place.shift):
                                self.exchange_shift(shift_place,extra_vigilant,available_vigilant)
                                if available_vigilant.id not in solution.sites_schedule[shift_place.site_id-1].assigned_Vigilantes:
                                    solution.sites_schedule[shift_place.site_id-1].assigned_Vigilantes[available_vigilant.id] = available_vigilant
                                if shift_place.site_id not in extra_vigilant.sites_to_look_out:
                                    solution.sites_schedule[shift_place.site_id-1].assigned_Vigilantes.pop(extra_vigilant.id)

                                if available_vigilant.total_hours_worked_by_week[index_week] >= MAXIMUM_EXTRA_WORKING_AMOUNT_HOURS_BY_WEEK:
                                    available_vigilantes[index_week].remove(available_vigilant)
                                    index_available_vigilant-=1
                                if extra_vigilant.total_hours_worked_by_week[index_week] == 0:
                                    extra_vigilantes_by_week[index_week].remove(extra_vigilant)
                                    index_vigilant-=1
                                if STOP_GRASP_TWEAK:
                                    return solution
                                break
                            index_available_vigilant+=1    
                        if extra_vigilant.total_hours_worked_by_week[index_week] == 0:
                            if STOP_GRASP_TWEAK:
                                return solution
                            break                
                index_vigilant+=1                    
        #Quitarle los shifts y asignarselos a algun otro guardia con 48 horas o mas
        self.delete_vigilantes_in_extra(extra_vigilantes_by_week, solution)
        return solution

    def assing_shifts_between_vigilantes_with_extra_hours_and_greater_than_24(self, extra_vigilant: Vigilant, vigilantes_with_extra_hours_in_week : List[Vigilant], solution: Solution, week):
        #Este esta bien ya
        index = 0
        while index < len(vigilantes_with_extra_hours_in_week):
            vigilant_with_extra_hour = vigilantes_with_extra_hours_in_week[index]
            shifts = vigilant_with_extra_hour.get_shifts_on_week(week+1)
            random.shuffle(shifts)
            for shift_place in shifts:  
                hoursShift = shift_place.shift.shift_end - shift_place.shift.shift_start + 1
                if vigilant_with_extra_hour.total_hours_worked_by_week[week] - hoursShift < MAXIMUM_WORKING_AMOUNT_HOURS_BY_WEEK:
                    continue 
                if self.vigilant_assigment_service.is_vigilant_avaible_tweaks(extra_vigilant, shift_place.shift):
                    self.exchange_shift(shift_place,vigilant_with_extra_hour,extra_vigilant)
                    vigiliantes_in_site = solution.sites_schedule[shift_place.site_id-1].assigned_Vigilantes

                    #Se agrega el vigilante sobrante al sitio sino estaba asginado
                    if extra_vigilant.id not in vigiliantes_in_site:
                        vigiliantes_in_site[extra_vigilant.id] = extra_vigilant
                    #Se elimina el vigilante con horas extras de el sitio si ya no tienen ningun shift
                    if shift_place.site_id not in vigilant_with_extra_hour.sites_to_look_out:
                        vigiliantes_in_site.pop(vigilant_with_extra_hour.id)

                    if vigilant_with_extra_hour.total_hours_worked_by_week[week] <= MAXIMUM_WORKING_AMOUNT_HOURS_BY_WEEK:
                        vigilantes_with_extra_hours_in_week.remove(vigilant_with_extra_hour)
                        index-=1
                        break
                    if extra_vigilant.total_hours_worked_by_week[week] >= MAXIMUM_WORKING_AMOUNT_HOURS_BY_WEEK:
                        break
            if extra_vigilant.total_hours_worked_by_week[week] >= MAXIMUM_WORKING_AMOUNT_HOURS_BY_WEEK:
                vigilantes_with_extra_hours_in_week.append(extra_vigilant)
                return True
            index+=1
        return False
    

    def assing_shifts_between_extra_vigilantes_greater_than(self, extra_vigilant: Vigilant, extra_vigilantes_by_week: List[List[Vigilant]], index_week: int, available_vigilantes: List[List[Vigilant]], solution: Solution):
        #Get vigilantes < to 24 and later the  > 24
        vigilantes_deleted = 0
        index_extra_vigilantes = 0
        while index_extra_vigilantes < len(extra_vigilantes_by_week[index_week]):
            other_extra_vigilant = extra_vigilantes_by_week[index_week][index_extra_vigilantes]
            if other_extra_vigilant.id == extra_vigilant.id:
                index_extra_vigilantes+=1
                continue
            shifts = other_extra_vigilant.get_shifts_on_week(index_week+1)
            for shift_place in shifts:
                if self.vigilant_assigment_service.is_vigilant_avaible_tweaks(extra_vigilant, shift_place.shift):
                    self.exchange_shift(shift_place,other_extra_vigilant,extra_vigilant)
                    if extra_vigilant.id not in solution.sites_schedule[shift_place.site_id-1].assigned_Vigilantes:
                        solution.sites_schedule[shift_place.site_id-1].assigned_Vigilantes[extra_vigilant.id] = extra_vigilant
                    if shift_place.site_id not in other_extra_vigilant.sites_to_look_out:
                        solution.sites_schedule[shift_place.site_id-1].assigned_Vigilantes.pop(other_extra_vigilant.id)                       

                    if other_extra_vigilant.total_hours_worked_by_week[index_week] == 0:
                        index_actual = extra_vigilantes_by_week[index_week].index(extra_vigilant)
                        index_delete = extra_vigilantes_by_week[index_week].index(other_extra_vigilant)
                        extra_vigilantes_by_week[index_week].remove(other_extra_vigilant)
                        if index_actual >= index_delete:
                            index_extra_vigilantes=-1
                        vigilantes_deleted=+1
                    
                    if extra_vigilant.total_hours_worked_by_week[index_week] >= MAXIMUM_WORKING_AMOUNT_HOURS_BY_WEEK:
                        if other_extra_vigilant not in extra_vigilantes_by_week[index_week]:
                            index_actual = index_delete
                            index_delete = extra_vigilantes_by_week[index_week].index(extra_vigilant)
                        else:
                            index_actual = extra_vigilantes_by_week[index_week].index(other_extra_vigilant)
                            index_delete = extra_vigilantes_by_week[index_week].index(extra_vigilant)
                        extra_vigilantes_by_week[index_week].remove(extra_vigilant)
                        if index_actual >= index_delete:
                            index_extra_vigilantes=-1
                        vigilantes_deleted=+1
                        available_vigilantes[index_week].append(extra_vigilant)
                        break
            if extra_vigilant.total_hours_worked_by_week[index_week] >= MAXIMUM_WORKING_AMOUNT_HOURS_BY_WEEK:
               break
            index_extra_vigilantes+=1
        return vigilantes_deleted
    
    def exchange_shift(self,shift: Shift_place, vigilant_to_remove_shift: Vigilant, vigilant_to_add_shift: Vigilant) -> None:
        shift.shift.change_vigilant(vigilant_to_remove_shift.id, vigilant_to_add_shift.id)
        vigilant_to_remove_shift.remove_shift(shift)
        vigilant_to_add_shift.assign_shift(shift.shift,shift.site_id)

    def get_extra_vigilantes_by_week(self, vigilantes: List[Vigilant]) -> List[List[Vigilant]]:
        extra_vigilantes_by_week: List[List[Vigilant]] = np.array([[]]* settings.MAX_TOTAL_WEEKS, dtype=object).tolist() 
        for vigilant in vigilantes:
            for index_week,hours_worked_on_week in enumerate(vigilant.total_hours_worked_by_week):
                if hours_worked_on_week < MAXIMUM_WORKING_AMOUNT_HOURS_BY_WEEK and hours_worked_on_week > 0:
                    extra_vigilantes_by_week[index_week].append(vigilant)
        return extra_vigilantes_by_week

    def get_available_vigilantes_by_week(self, vigilantes: List[Vigilant]) -> List[List[Vigilant]]:
        available_vigilantes_by_week: List[List[Vigilant]] = np.array([[]]* settings.MAX_TOTAL_WEEKS, dtype=object).tolist() 
        for vigilant in vigilantes:
            for index_week,hours_worked_on_week in enumerate(vigilant.total_hours_worked_by_week):
                if hours_worked_on_week >= MAXIMUM_WORKING_AMOUNT_HOURS_BY_WEEK and hours_worked_on_week <= MAXIMUM_EXTRA_WORKING_AMOUNT_HOURS_BY_WEEK:
                    available_vigilantes_by_week[index_week].append(vigilant)
        return available_vigilantes_by_week

    def delete_vigilantes_in_extra(self, extra_vigilantes_by_week: List[List[Vigilant]], solution: Solution):
        total_weeks = len(extra_vigilantes_by_week)
        vigilantes_extras: List[Vigilant] = []
        for extra_vigilantes_on_week in extra_vigilantes_by_week:
            for vigilant in extra_vigilantes_on_week:
                if vigilant not in vigilantes_extras:
                    vigilantes_extras.append(vigilant)
        if len(vigilantes_extras) > 1:
            random.shuffle(vigilantes_extras)
            index_vigilant = 0
            while index_vigilant + 1< len(vigilantes_extras):
                actual_vigilant = vigilantes_extras[index_vigilant]
                index_vigilant_taken = index_vigilant + 1
                while index_vigilant_taken < len(vigilantes_extras):
                    vigilant_to_take = vigilantes_extras[index_vigilant_taken]
                    shifts = vigilant_to_take.shifts
                    for shift_place in shifts:
                        if self.vigilant_assigment_service.is_vigilant_avaible_tweaks(actual_vigilant, shift_place.shift):
                            self.exchange_shift(shift_place,vigilant_to_take,actual_vigilant)
                            if actual_vigilant.id not in solution.sites_schedule[shift_place.site_id-1].assigned_Vigilantes:
                                solution.sites_schedule[shift_place.site_id-1].assigned_Vigilantes[actual_vigilant.id] = actual_vigilant
                            if shift_place.site_id not in vigilant_to_take.sites_to_look_out:
                                solution.sites_schedule[shift_place.site_id-1].assigned_Vigilantes.pop(vigilant_to_take.id)
                            
                            if vigilant_to_take.total_hours_worked == 0:
                                vigilantes_extras.remove(vigilant_to_take)
                                index_vigilant_taken-=1
                            if actual_vigilant.total_hours_worked == MAXIMUM_WORKING_AMOUNT_HOURS_BY_WEEK * total_weeks:
                                break
                    if actual_vigilant.total_hours_worked == MAXIMUM_WORKING_AMOUNT_HOURS_BY_WEEK * total_weeks:
                        break
                    index_vigilant_taken+=1
                vigilantes_extras.remove(actual_vigilant)