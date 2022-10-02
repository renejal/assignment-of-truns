
import random
from typing import List, Tuple

import numpy as np
from conf import settings
from dominio.Solution import Solution
from dominio.model.shift_place import Shift_place
from dominio.model.vigilant import Vigilant
from services.vigilant_assigment_service import Vigilant_assigment_service

class Tweak_extra_hours:
    vigilant_assigment_service = Vigilant_assigment_service(None)
    #Cuestionarse si encuentra un vigilante continuar con el o volver a resetear las prioridades? creo que es mejor resetear las prioridades caso de 32 horas paso a 40
    #deberia seguir con otro que quedo en menos prioridad.
    #Cuestionarse si shufleo y no les doy prioridad
    #Asignarle un shift a otro guardia con menos horas de trabajo
    def extra_hours_tweak(self, solution: Solution)-> Solution:
        #Empezar con aquellos guardias que tengan menos de 40 horas
        # con aquellos guardias que tengan entre 40 y 48 horas
        #Escoger guardias que tengan 0 horas trabajas.
        vigilantes_with_hours_to_work: List[List[List[Vigilant]]] = self.get_available_vigilantes_to_work_by_prioritys(solution.vigilantes_schedule)
        vigilantes_with_extra_hours: List[List[Vigilant]] = self.get_vigilantes_with_extra_hours_by_week(solution.vigilantes_schedule)    
        for index_week, vigilantes_with_extra_hours_on_week in enumerate(vigilantes_with_extra_hours):
            random.shuffle(vigilantes_with_extra_hours_on_week)
            for vigilant_with_extra_hours_on_week in vigilantes_with_extra_hours_on_week:
                shifts_by_week = vigilant_with_extra_hours_on_week.get_shifts_on_week(index_week+1)
                random.shuffle(shifts_by_week)
                for index_priority, vigilantes_by_priority_on_week in enumerate(vigilantes_with_hours_to_work[index_week]):
                    random.shuffle(vigilantes_by_priority_on_week)
                    index = 0
                    while index < len(vigilantes_by_priority_on_week):
                        available_vigilant_on_week = vigilantes_by_priority_on_week[index]
                        for shift in shifts_by_week:
                            if self.vigilant_assigment_service.is_vigilant_avaible(available_vigilant_on_week,shift.shift):
                                self.exchange_shift(shift,vigilant_with_extra_hours_on_week,available_vigilant_on_week)
                                if available_vigilant_on_week.id not in solution.sites_schedule[shift.site_id-1].assigned_Vigilantes:
                                    solution.sites_schedule[shift.site_id-1].assigned_Vigilantes[available_vigilant_on_week.id] = available_vigilant_on_week
                                if shift.site_id not in vigilant_with_extra_hours_on_week.sites_to_look_out:
                                    solution.sites_schedule[shift.site_id-1].assigned_Vigilantes.pop(vigilant_with_extra_hours_on_week.id)
                                #Chequar si el vigilante ya no puede trabajar mas horas en la semana
                                if available_vigilant_on_week.total_hours_worked_by_week[index_week] >= 48:
                                    vigilantes_by_priority_on_week.remove(available_vigilant_on_week)
                                    index -= 1
                                    break
                                if index_priority == 0 and available_vigilant_on_week.total_hours_worked_by_week[index_week] >= 40:
                                    vigilantes_by_priority_on_week.remove(available_vigilant_on_week)
                                    index -= 1
                                    vigilantes_with_hours_to_work[index_week][1].append(available_vigilant_on_week)
                                    break
                                #Chequear si el vigilante con extra horas ya no tiene horas extras
                                if vigilant_with_extra_hours_on_week.total_hours_worked_by_week[index_week] <= 48:
                                    break
                        if vigilant_with_extra_hours_on_week.total_hours_worked_by_week[index_week] <= 48: 
                            break        
                        index += 1
                    else:
                        continue
                    break
        return solution

    def exchange_shift(self,shift: Shift_place,vigilant_with_extra_hours_on_week: Vigilant, vigilant_with_hour_to_work: Vigilant) -> None:
        shift.shift.change_vigilant(vigilant_with_extra_hours_on_week.id, vigilant_with_hour_to_work.id)
        vigilant_with_extra_hours_on_week.remove_shift(shift)
        vigilant_with_hour_to_work.assign_shift(shift.shift,shift.site_id)

    def  get_available_vigilantes_to_work_by_prioritys(self,vigilantes: List[Vigilant]) -> List[List[List[Vigilant]]]:
        vigilantes_with_hours_to_work: List[List[List[Vigilant]]] =  np.array([[[],[],[]]]* settings.MAX_TOTAL_WEEKS, dtype=object).tolist() 
        range_prioritys: List[Tuple] = [(1,39),(40,55),(0,0)]
        for vigilant in vigilantes:
            for index_range, range in enumerate(range_prioritys):
                for index_week,hours_worked_by_week in enumerate(vigilant.total_hours_worked_by_week):
                    if hours_worked_by_week >= range[0] and hours_worked_by_week <= range[1] :
                        vigilantes_with_hours_to_work[index_week][index_range].append(vigilant)
        return vigilantes_with_hours_to_work 

    def get_vigilantes_with_extra_hours_by_week(self, vigilantes: List[Vigilant]) -> List[List[Vigilant]]:
        vigilantes_with_extra_hours_by_week = np.array([[]]* settings.MAX_TOTAL_WEEKS, dtype=object).tolist() 
        for vigilant in vigilantes:
            for index, hours_worked_on_week in enumerate(vigilant.total_hours_worked_by_week):
                if hours_worked_on_week > 48:
                    vigilantes_with_extra_hours_by_week[index].append(vigilant)
        return vigilantes_with_extra_hours_by_week