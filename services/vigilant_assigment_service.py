from dominio.model.site import Site
from conf import settings
from dominio.vigilant_assigment import VigilantAssigment
from utils import aleatory
from typing import List, Dict
from dominio.model.vigilant import Vigilant
from dominio.model.shift import Shift
import math

class Vigilant_assigment_service:

<<<<<<< HEAD
    def get_possible_vigilant_to_assign(site: int, vigilantes: List[Vigilant]) -> int:
=======
    def is_vigilant_avaible(self,vigilant: Vigilant, shift:Shift) -> bool:
        if self.is_available_on_shift(vigilant,shift) == False:
            return False 
        if self.has_enough_hours_to_work_in_week(vigilant, shift) == False:
            return False
        #Check work on sunday
        return True          
        
    def is_available_on_shift(self,vigilant: Vigilant,shift: Shift):
        shifts_vigilant:List[Shift] = vigilant.shifts
        if len(shifts_vigilant) ==0:
            return True
        for index, assigned_shift in enumerate(shifts_vigilant):
            if shift.shift_end < assigned_shift.shift_start:
                if index > 0:
                    return shift.shift_end + 18 <  assigned_shift.shift_start and shift.shift_start - 18 > shifts_vigilant[index].shift_end
                return shift.shift_end + 18 <  assigned_shift.shift_start
        return shift.shift_start - 18 > shifts_vigilant[index].shift_end


     #Check restrictions   
    
    def has_enough_hours_to_work_in_week(self,vigilant: Vigilant, shift: Shift):
        start_week_of_shift = math.floor(shift.shift_start/168)
        end_week_of_shift  =  math.floor(shift.shift_end/168)
        total_hours_worked_by_vigilant_each_week = vigilant._total_hours_worked_by_week

        if start_week_of_shift == end_week_of_shift:
            if  (total_hours_worked_by_vigilant_each_week[start_week_of_shift]+(shift.shift_end - shift.shift_start)) <= VigilantAssigment.maxWorkHoursPerWeek:
                return True
            return False
        else:
            if (total_hours_worked_by_vigilant_each_week[start_week_of_shift]+(168*end_week_of_shift)-shift.shift_start) <= VigilantAssigment.maxWorkHoursPerWeek and (total_hours_worked_by_vigilant_each_week[end_week_of_shift]+shift.shift_end-(168*end_week_of_shift)) <= VigilantAssigment.maxWorkHoursPerWeek:
                return True
        return False
    
    def canWorkThisSunday(self,startPeriod,endPeriod):
        weekToCheck = math.floor(startPeriod/168)
        if self.thereIsAPeriodInSunday(startPeriod,endPeriod,weekToCheck):
            return self.workLastSunday(weekToCheck)
        return True
    
    def workLastSunday(self,week):
        if week == 0:
            return True
        for period in range (168*week,(168*week)-24,-1):
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
   
    def get_possible_vigilant_to_assign(site: Site, vigilantes: List[Vigilant]) -> int:
>>>>>>> 4d2a388f4a9dce52c4e09a5c053bd2fc2df1869c
        """
        obtain random vigilant for parametr the settings
        vigilantes: list de vigilantes total
        Site: sitio a vigilar
        shift: los turnos del sitio a vigilar

        return the possible vigilantes avalaible for site
        """

        dict_vigilants_distance: Dict = Vigilant_assigment_service.__order_vigilants_in_place_by_distance(vigilantes, site)
        vigilants_id: int = aleatory.get_ramdon_for_list(0, settings.WINDOWS_RANDOM_THE_VIGILANTS_ORDER_FOR_SITE,
                                                         dict_vigilants_distance)
        return vigilants_id

    def __order_vigilants_in_place_by_distance(vigilantes: List[Vigilant], site_id: int) -> Dict:
        """
        :param vigilantes:
        :param site:
        :return: List the Dict {vigilans_id : vigilants.distancia }
        """
        dict_order_the_vigilants_for_distance: Dict = {}
        vigilant: Vigilant
        for vigilant in range(0, len(vigilantes)):
            dict_order_the_vigilants_for_distance[vigilant.id] = vigilant.distance[site_id]

        return dict_order_the_vigilants_for_distance

    def __obtain_vigilants_in_default_for_site(vigilants: List[Vigilant], site_id: int) -> List:
        """
        obtain vigilants for default for the site whit id = n

        :param vigilants: list the vigilants
        :param site_id: identy vigilants
        :return: vigilants for default
        """
        vigilant_for_default: List = []
        for vigilant in vigilants:
            if vigilant.default_place_to_look_out == site_id:
                vigilant_for_default[vigilant.id] = vigilant.distance[site_id]
        settings.random.shuffle(vigilant_for_default)
        return vigilant_for_default
