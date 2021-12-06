from typing import Dict, List
# from data.SiteDataFile import SiteDataFile
# from data.VigilantsDataFile import VigilantsDataFile
from dominio.model.site import Site
from dominio.model.vigilant import Vigilant
from dominio.model.shift import Shift

import operator


class VigilantAssigment:
    # maxShiftDuration: int = 12
    # minShiftDuration: int = 4
    # minBreakDuration: int = 18
    # maxOvertimeWorkHoursPerWeek=12
    # maxWorkHoursPerWeek=48
    # minWorkHoursPerWeek=40
    # idealWorkHoursPerWeek=48

    vigilantes: List[Vigilant]
    sites: List[Site]
    total_vigilantes: int
    total_sites: int
    total_weeks: int 
    expectec_places_to_look_out_by_vigilants: Dict[int, List[int]]
    order_sites_by_id_vigilantes_amount: List[int]
    shifts_by_sites: List[List[Shift]]

    __DEFAULT_PLACE_TO_LOOK_OUT_FORMAT: int = -1
    __END_HOUR_TO_WORK: int = 23
    __MAX_HOURS_TO_WORK: int= 24 

    def __init__(self, vigilantes: List[Vigilant], sites: List[Site], weeks) -> None:
        self.vigilantes = vigilantes
        self.sites = sites
        self.total_weeks = weeks
        self.total_sites = len(sites)
        self.expectec_places_to_look_out_by_vigilants = {}
        self.initProblem()

    def initProblem(self) -> None:

        for vigilant in self.vigilantes:
            if vigilant.default_place_to_look_out != self.__DEFAULT_PLACE_TO_LOOK_OUT_FORMAT:
                if vigilant.default_place_to_look_out in self.expectec_places_to_look_out_by_vigilants:
                    self.expectec_places_to_look_out_by_vigilants[vigilant.default_place_to_look_out].apppend(vigilant.id)
                else:
                    self.expectec_places_to_look_out_by_vigilants[vigilant.default_place_to_look_out] = vigilant.id
        self.shifts_by_sites = self.create_shifts_by_site(self.sites)
        self.order_sites_by_id_vigilantes_amount = self.sorted_sites_by_vigilant_amount(self.shifts_by_sites)

    def create_ideal_hours_amount_to_work(self) -> Dict[int,List[int]]: 
        return { 0:[], 1:[1],2:[2],3:[3],4:[4],5:[5],6:[6], 7:[7],8:[8],9:[9],10:[10],11:[11],12:[12],13:[7,6],14:[7,7],15:[8,7],16:[8,8],17:[8,9],18:[9,9],19:[10,9],20:[10,10],21:[7,7,7],22:[8,7,7],
                      23:[8,8,7],24:[8,8,8]}

    def create_shifts_by_site(self, sites: List[Site]) -> List[List[Shift]]:
        ideal_hours_amount_to_work = self.create_ideal_hours_amount_to_work()
        shifts_by_site : List[List[Shift]] = [] 
        for site in sites:
            shifts_by_site.append([])
            last_day_finished_at_end_hour_to_work = False
            for index_week , week in enumerate(site.weeks_schedule):
                for index_day, day in enumerate(week.days):
                    for shift in day.working_day:
                        if last_day_finished_at_end_hour_to_work == False:
                            shift_start_time =  shift.working_start + day.id * 24 + index_week * 168
                        if( shift.working_end == self.__END_HOUR_TO_WORK and index_day+1 < len(week.days) and week.days[index_day + 1].id == day.id+1 and week.days[index_day + 1].working_day[0].working_start == 0):
                            working_hours_amount =  shift.working_end - shift.working_start +  week.days[index_day + 1].working_day[0].working_end
                            if working_hours_amount > self.__MAX_HOURS_TO_WORK:
                                working_hours_amount = self.__MAX_HOURS_TO_WORK     
                            last_day_finished_at_end_hour_to_work = True
                        else:
                            if day.id == 6 and index_week + 1 < self.total_weeks and  site.weeks_schedule[index_week+1].days[0].working_day[0].working_start == 0:
                                working_hours_amount = shift.working_end - shift.working_start + site.weeks_schedule[index_week].days[0].working_day[0].working_end
                                if working_hours_amount > self.__MAX_HOURS_TO_WORK:
                                    working_hours_amount = self.__MAX_HOURS_TO_WORK     
                                last_day_finished_at_end_hour_to_work = True
                            else: 
                                if last_day_finished_at_end_hour_to_work:
                                    working_hours_amount =  (shift.working_end + day.id*24 + index_week*168) - shift_start_time 
                                    if shift.working_end == 23:
                                        working_hours_amount = shift.working_end + 1
                                else:
                                    working_hours_amount =  shift.working_end -  shift.working_start + 1
                                last_day_finished_at_end_hour_to_work = False
                        hours_amount_to_work_by_shift = ideal_hours_amount_to_work[working_hours_amount]
                        for hours_amount_to_work in hours_amount_to_work_by_shift:
                            shifts_by_site[site.id-1].append(Shift( shift_start_time , shift_start_time + hours_amount_to_work -1  , shift.num_vigilantes))
                            shift_start_time += hours_amount_to_work
        return shifts_by_site

    def get_vigilantes_needed_by_site(self,shifts_by_sites) -> Dict[int,int]:
        vigilantes_needed_by_site = {}
        for indexSite, site_shifts in enumerate(shifts_by_sites):
            acc = 0
            for shift in site_shifts:
                acc += shift.necesary_vigilantes
            vigilantes_needed_by_site[indexSite + 1] = acc
        return vigilantes_needed_by_site

    def get_order_site_by_vigilantes_amount(self, pos: int) -> int:
        return self.getSite(self.order_sites_by_id_vigilantes_amount[pos])

    def sorted_sites_by_vigilant_amount(self, shifts_by_sites ):
        vigilantes_needed_by_site = self.get_vigilantes_needed_by_site(shifts_by_sites)
        vigilantes_needed_sorted_by_site = sorted(vigilantes_needed_by_site.items(), key=operator.itemgetter(1), reverse=True)
        order_sites = []
        for i in vigilantes_needed_sorted_by_site:
            order_sites.append(int(i[0]))
        return order_sites

    def get_shifts_on_site(self, site_id:int) -> List[Shift]:
        return self.shifts_by_sites[site_id-1]

    def getSite(self, siteId) -> int:
        return self.sites[siteId-1].id

   