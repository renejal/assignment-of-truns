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
    _MAXIMUM_WORKING_AMOUNT_HOURS_BY_WEEK=48


    def is_vigilant_avaible(self, vigilant: Vigilant, shift:Shift) -> bool:
        if self.has_enough_hours_to_work_in_week(vigilant, shift) == False:
            return False
        if self.is_available_on_shift(vigilant, shift) == False:
            return False 
        #Check work on sunday
        return True          
        
    def is_available_on_shift(self, vigilant: Vigilant,shift: Shift):
        shifts_vigilant:List[Shift] = vigilant.shifts
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
   
    # def get_possible_vigilant_to_assign(site: Site, vigilantes: List[Vigilant],) -> int:
    def get_possible_vigilant_to_assign(**kwargs):
        """
        obtain random vigilant for parametr the settings
        vigilants: list de vigilantes total
        site_id: sitio a vigilar
        vigilants_temp : None

        return the possible vigilant id avalaible for site
        """
        vigilants_temp: List = kwargs.get("vigilants_temp")
        vigilants: List[Vigilant] = kwargs.get("vigilants")
        site_id: int = kwargs.get("site_id")
        vigilants_id: int
        dict_vigilants_distance: Dict

        if vigilants is not None:
            print("no se encontraron vigilantes")
            raise
        if vigilants_temp is not None:
            vigilants_id = aleatory.get_ramdon_for_list(0, settings.WINDOWS_RANDOM_THE_VIGILANTS_ORDER_FOR_SITE, dict_vigilants_distance)

        vigilants_temp = copy.deepcopy(vigilants)
        if vigilants_temp is not None:
            dict_vigilants_distance = Vigilant_assigment_service.__order_vigilants_in_place_by_distance(vigilants_temp, site_id)
            vigilants_id = aleatory.get_ramdon_for_list(0, settings.WINDOWS_RANDOM_THE_VIGILANTS_ORDER_FOR_SITE, dict_vigilants_distance)


        return vigilants_id, vigilants_temp

    def __order_vigilants_in_place_by_distance(vigilants: List[Vigilant], site_id: int) -> Dict:
        """
        :param vigilants:
        :param site_id:
        :return: List the Dict {vigilans_id : vigilants.distancia }
        """
        dict_order_the_vigilants_for_distance: Dict = {}
        vigilant: Vigilant
        for vigilant in range(0, len(vigilants)):
            dict_order_the_vigilants_for_distance[vigilant.id] = vigilant.distance[site_id]
        dict_order_the_vigilants_for_distance = sorted(dict_order_the_vigilants_for_distance)

        return dict_order_the_vigilants_for_distance

    def obtain_vigilants_in_default_for_site(vigilants: List[Vigilant], site_id: int) -> List:
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

        return copy.deepcopy(vigilant_for_default)
