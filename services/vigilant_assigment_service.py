from dominio.model.site import Site
from conf import settings
from dominio.vigilant_assigment import VigilantAssigment
from utils import aleatory
from typing import List, Dict
import copy
from dominio.model.vigilant import Vigilant
from dominio.model.shift import Shift
import math

class Vigilant_assigment_service:

    _MINIMUN_BREAK_DURATION: int = 18
    _MAXIMUM_WORKING_AMOUNT_HOURS_BY_WEEK: int = 48

    vigilant_assigment: VigilantAssigment

    def __init__(self, vigilant_assigment: VigilantAssigment):
        self.vigilant_assigment = vigilant_assigment

    def is_vigilant_avaible(self, vigilant: Vigilant, shift:Shift) -> bool:
        if self.has_enough_hours_to_work_in_week(vigilant, shift) == False:
            return False
        if self.is_available_on_shift(vigilant, shift) == False:
            return False 
        #Check work on sunday
        return True          
        
    def is_available_on_shift(self, vigilant: Vigilant,shift: Shift):
        shifts_vigilant:List[Shift] = list(vigilant.shifts.keys())
        if len(shifts_vigilant) == 0:
            return True
        for index, assigned_shift in enumerate(shifts_vigilant):
            if shift.shift_end < assigned_shift.shift_start:
                if index > 0:
                    return shift.shift_end + self._MINIMUN_BREAK_DURATION <  assigned_shift.shift_start and shift.shift_start - self._MINIMUN_BREAK_DURATION > shifts_vigilant[index-1].shift_end
                return shift.shift_end + self._MINIMUN_BREAK_DURATION <  assigned_shift.shift_start
        return shift.shift_start - self._MINIMUN_BREAK_DURATION > shifts_vigilant[index].shift_end


     #Check restrictions   
    
    def has_enough_hours_to_work_in_week(self,vigilant: Vigilant, shift: Shift):
        start_week_of_shift = math.floor(shift.shift_start/168)
        end_week_of_shift  =  math.floor(shift.shift_end/168)
        total_hours_worked_by_vigilant_each_week = vigilant.total_hours_worked_by_week
        if start_week_of_shift == end_week_of_shift:
            if  (total_hours_worked_by_vigilant_each_week[start_week_of_shift]+(shift.shift_end - shift.shift_start + 1)) <= self._MAXIMUM_WORKING_AMOUNT_HOURS_BY_WEEK:
                return True
            return False
        else:
            if (total_hours_worked_by_vigilant_each_week[start_week_of_shift]+(168*end_week_of_shift)-shift.shift_start) <= self._MAXIMUM_WORKING_AMOUNT_HOURS_BY_WEEK and (total_hours_worked_by_vigilant_each_week[end_week_of_shift]+shift.shift_end-(168*end_week_of_shift - 1)) <= self._MAXIMUM_WORKING_AMOUNT_HOURS_BY_WEEK:
                return True
        return False
    
    def canWorkThisSunday(self, startPeriod, endPeriod):
        weekToCheck = math.floor(startPeriod/168)
        if self.thereIsAPeriodInSunday(startPeriod, endPeriod, weekToCheck):
            return self.workLastSunday(weekToCheck)
        return True
    
    def workLastSunday(self,week):
        if week == 0:
            return True
        for period in range(168*week, (168*week)-24, -1):
            if self.shifts[period] != 0:
                return False
        return True
    
    def thereIsAPeriodInSunday(self,startPeriod,endPeriod,week):
        if (startPeriod > 144+ (168*week) and startPeriod < 168*(week+1)):
            return True
        else:
            if (endPeriod > 144+ (168*week)):
              return True
        return False

    def check_if_vigilant_has_missing_hours(self, vigilant: Vigilant):
        for hour_by_week in vigilant.total_hours_worked_by_week:
             if hour_by_week < 40:
                 return True
        return False

    def get_order_vigilantes_index_in_place_by_distance(self, site_id: int, vigilantes: List[Vigilant]) -> List[Vigilant]:
        index_vigilants = [vID for vID in self.vigilant_assigment.order_sites_by_id_vigilantes_distance[site_id -1] if vigilantes[vID-1].default_place_to_look_out == site_id or vigilantes[vID-1].default_place_to_look_out == -1]
        return [v for v in vigilantes if v.id in index_vigilants]

    def obtain_vigilants_in_default_for_site(self, site_id: int, vigilantes: List[Vigilant]) -> List[Vigilant]:
        if site_id in self.vigilant_assigment.expected_places_to_look_out_by_vigilants:
            expected_vigilantes_by_place: List[Vigilant] = []
            for vigilant_id in  self.vigilant_assigment.expected_places_to_look_out_by_vigilants.get(site_id):
                expected_vigilantes_by_place.append(vigilantes[vigilant_id-1])
            return expected_vigilantes_by_place
        return None