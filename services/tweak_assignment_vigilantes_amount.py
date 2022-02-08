from typing import List

import numpy as np
from conf.settings import MAX_TOTAL_WEEKS
from dominio.Solution import Solution
from dominio.model.shift_place import Shift_place
from dominio.model.vigilant import Vigilant
from services.vigilant_assigment_service import Vigilant_assigment_service


class Tweak_assignment_vigilantes_amount:
    vigilant_assigment_service = Vigilant_assigment_service(None)

    #Deberia asignarle las horas de los vigilantes extras primero a los de entre 40-48 y luego a los de 48-55?
    def assignment_vigilantes_amount(self, solution: Solution) -> Solution:
        #Obtener vigilantes que tienen menos de 40 horas
        extra_vigilantes_by_week: List[List[Vigilant]] = self.get_extra_vigilantes_by_week(solution.vigilantes_schedule)
        available_vigilantes: List[List[Vigilant]] = self.get_available_vigilantes_by_week(solution.vigilantes_schedule)
        for index_week, extra_vigilantes_on_week in enumerate(extra_vigilantes_by_week):
            for extra_vigilant in extra_vigilantes_on_week:
                shifts = extra_vigilant.get_shifts_on_week(index_week+1)
                for shift_place in shifts:
                    for available_vigilant in available_vigilantes[index_week]:
                        if self.vigilant_assigment_service.is_vigilant_avaible(available_vigilant, shift_place.shift):
                            self.exchange_shift(shift_place,extra_vigilant,available_vigilant)
                            if available_vigilant.total_hours_worked_by_week[index_week] >= 56:
                                available_vigilantes[index_week].remove(available_vigilant)
                            break
        return solution
    
    def exchange_shift(self,shift: Shift_place, vigilant_to_remove_shift: Vigilant, vigilant_to_add_shift: Vigilant) -> None:
        shift.shift.change_vigilant(vigilant_to_remove_shift.id, vigilant_to_add_shift.id)
        vigilant_to_remove_shift.remove_shift(shift)
        vigilant_to_add_shift.assign_shift(shift.shift,shift.site_id)


    def get_extra_vigilantes_by_week(self, vigilantes: List[Vigilant]) -> List[List[Vigilant]]:
        extra_vigilantes_by_week: List[List[Vigilant]] = np.array([[]]* MAX_TOTAL_WEEKS, dtype=object).tolist() 
        for vigilant in vigilantes:
            for index_week,hours_worked_on_week in enumerate(vigilant.total_hours_worked_by_week):
                if hours_worked_on_week < 40 and hours_worked_on_week > 0:
                    extra_vigilantes_by_week[index_week].append(vigilant)
        return extra_vigilantes_by_week

    def get_available_vigilantes_by_week(self, vigilantes: List[Vigilant]) -> List[List[Vigilant]]:
        available_vigilantes_by_week: List[List[Vigilant]] = np.array([[]]* MAX_TOTAL_WEEKS, dtype=object).tolist() 
        for vigilant in vigilantes:
            for index_week,hours_worked_on_week in enumerate(vigilant.total_hours_worked_by_week):
                if hours_worked_on_week >= 40 and hours_worked_on_week < 56:
                    available_vigilantes_by_week[index_week].append(vigilant)
        return available_vigilantes_by_week

