import math
from typing import Dict, List
from dominio.model.site import Site
from dominio.model.shift import Shift

class Shifts_generation_service:

    __END_HOUR_TO_WORK: int = 23
    __MAX_HOURS_TO_WORK: int= 24 

    def create_shifts_by_site(self, sites: List[Site]) -> List[List[Shift]]:
        ideal_hours_amount_to_work = self.create_ideal_hours_amount_to_work()
        shifts_by_site : List[List[Shift]] = [] 
        for site in sites:
            if site.is_special_site:
                shifts_by_site.append(self.create_shifts_in_special_site(site, site.total_weeks))
            else:
                shifts_data = self.create_shifts_in_normal_sites(site,ideal_hours_amount_to_work, site.total_weeks)
                shifts_by_site.append(shifts_data[0])
                self.calculate_max_fitness(site,shifts_data[1],shifts_data[2])
        return shifts_by_site

    def create_ideal_hours_amount_to_work(self) -> Dict[int,List[int]]: 
        return { 0:[], 1:[1],2:[2],3:[3],4:[4],5:[5],6:[6], 7:[7],8:[8],9:[9],10:[10],11:[11],12:[12],13:[7,6],14:[7,7],15:[8,7],16:[8,8],17:[8,9],18:[9,9],19:[10,9],20:[10,10],21:[7,7,7],22:[8,7,7],
                      23:[8,8,7],24:[8,8,8]}

    def create_shifts_in_normal_sites(self, site: Site , ideal_hours_amount_to_work: int, total_weeks:int) -> List[Shift]:
        shifts : list[Shift] = []
        total_missing_shifts = 0
        minimum_necessary_vigilantes = 0
        last_shift_finished_at_end_day = False
        shift_start_time = -1
        for index_week , week in enumerate(site.weeks_schedule):
            for index_day, day in enumerate(week.days):
                for shift in day.working_day:
                    shift_end_time = shift.working_end + day.id* 24 + index_week * 168
                    if shift_end_time - shift_start_time <= 0:
                        last_shift_finished_at_end_day = False
                        continue
                    if last_shift_finished_at_end_day == False:
                        shift_start_time = shift.working_start + day.id * 24 + index_week * 168
                    if shift.working_end == self.__END_HOUR_TO_WORK and index_day+1 < len(week.days) and week.days[index_day + 1].id == day.id+1 and week.days[index_day + 1].working_day[0].working_start == 0:
                        working_hours_amount =  shift.working_end - shift.working_start +  week.days[index_day + 1].working_day[0].working_end + 2
                        if working_hours_amount > self.__MAX_HOURS_TO_WORK:
                            working_hours_amount = self.__MAX_HOURS_TO_WORK
                        last_shift_finished_at_end_day = True     
                    elif shift.working_end == self.__END_HOUR_TO_WORK and day.id == 6 and index_week + 1 < total_weeks and site.weeks_schedule[index_week+1].days[0].id == 0 and site.weeks_schedule[index_week+1].days[0].working_day[0].working_start == 0:
                        working_hours_amount = shift.working_end - shift.working_start + site.weeks_schedule[index_week].days[0].working_day[0].working_end + 1
                        if working_hours_amount > self.__MAX_HOURS_TO_WORK:
                            working_hours_amount = self.__MAX_HOURS_TO_WORK
                        last_shift_finished_at_end_day = True     
                    else:                         
                        working_hours_amount =  shift_end_time - shift_start_time + 1
                        last_shift_finished_at_end_day = False
                    hours_amount_to_work_by_shift = ideal_hours_amount_to_work[working_hours_amount]
                    for index_shift, hours_amount_to_work in enumerate(hours_amount_to_work_by_shift):
                        shifts.append(Shift(index_shift, shift_start_time , shift_start_time + hours_amount_to_work -1  , shift.num_vigilantes))
                        shift_start_time += hours_amount_to_work
                        total_missing_shifts+=shift.num_vigilantes
                        minimum_necessary_vigilantes+=shift.num_vigilantes * hours_amount_to_work
        return shifts,total_missing_shifts,minimum_necessary_vigilantes
        
    def create_shifts_in_special_site(self,site: Site, total_weeks : int) -> List[Shift]:
        shifts : list[Shift] = []
        is_same_shift_that_last_day = False
        for index_week, week in enumerate(site.weeks_schedule):
            for index_day,day in enumerate(week.days):
                for index_shift, shift in enumerate(day.working_day):
                    if is_same_shift_that_last_day:
                        is_same_shift_that_last_day = False
                        continue                        
                    shift_start_time = shift.working_start + 24 * day.id + index_week * 168
                    shift_end_time = shift.working_end + 24 * day.id + index_week * 168
                    if (shift.working_end == self.__END_HOUR_TO_WORK and index_day+1 < len(week.days) and week.days[index_day + 1].id == day.id+1 and week.days[index_day + 1].working_day[0].working_start == 0 ) :
                        shift_end_time = week.days[index_day + 1].working_day[0].working_end + 24 * (day.id+1) + index_week * 168
                        is_same_shift_that_last_day = True
                    elif day.id == 6 and shift.working_end == self.__END_HOUR_TO_WORK and index_week + 1 < total_weeks and  site.weeks_schedule[index_week+1].days[0].working_day[0].working_start == 0:
                        shift_end_time = site.weeks_schedule[index_week+1].days[0].working_day[0].working_end + (index_week+1) * 168
                        is_same_shift_that_last_day = True
                    shifts.append(Shift(index_shift, shift_start_time , shift_end_time , shift.num_vigilantes))
        return shifts

    def calculate_max_fitness(self,site: Site, total_missing_shifts,minimum_necessary_vigilantes) -> None:
        site.total_missing_shifts = total_missing_shifts
        site.minimum_necessary_vigilantes = math.ceil(minimum_necessary_vigilantes/(40*site.total_weeks))
        site.calculate_max_extra_hours()