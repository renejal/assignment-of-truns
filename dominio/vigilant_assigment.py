from typing import Dict, List
# from data.SiteDataFile import SiteDataFile
# from data.VigilantsDataFile import VigilantsDataFile
from dominio.Site import Site
from dominio.vigilant import Vigilant
from dominio.Shift import Shift

import operator


class VigilantAssigment:
    maxShiftDuration: int = 12
    minShiftDuration: int = 4
    minBreakDuration: int = 18
    maxOvertimeWorkHoursPerWeek=12
    maxWorkHoursPerWeek=48
    minWorkHoursPerWeek=40
    idealWorkHoursPerWeek=48
    __vigilantes: List[Vigilant]
    __sites: List[Site]
    __total_vigilantes: int
    __total_sites: int
    __total_weeks: int 
    __vigilantExpectedPlaces: Dict[int, List[int]]
    __order_sites_by_vigilantes_amount: List[int]
    
    __END_HOUR_TO_WORK: int = 23
    __MAX_HOURS_TO_WORK: int= 24 

    def __init__(self, vigilantes: List[Vigilant], sites: List[Site], weeks) -> None:
        self.__vigilantes = vigilantes
        self.__sites = sites
        self.__total_weeks = weeks
        # TO DO OrderSites
        self.initProblem()

    def initProblem(self) -> None:
        for vigilant in self.__vigilantes:
            if vigilant != 0:
                if vigilant.__default_place_to_look_out:
                    self.__vigilantExpectedPlaces[vigilant.__default_place_to_look_out].apppend(vigilant.__vigilant_id)
                else:
                    self.__vigilantExpectedPlaces[vigilant.__default_place_to_look_out] = vigilant.__vigilant_id
        self.create_Shifts_By_Site(self.__sites)
        self.OrderSitesForCantVigilantes()

    def create_Shifts_By_Site(self, sites: List[Site]) -> List[List[Shift]]:
        workingDay = self.loadWorkingDay()
        shifts_by_site = List[List[Shift]]
        for site in sites:
            shifts_by_site.append(list[Shift])
            for week in site.weeks_schedule:
                for day in week:
                    for index, shift in enumerate(day.working_day):
                        shift_start_time =  shift.working_start
                        if( shift.working_end == self.__END_HOUR_TO_WORK and day.working_day[index+1].working_start == 0):
                            working_hours_amount =  shift.working_end - shift.working_start +  day.working_day[index+1].end
                            if working_hours_amount > self.__MAX_HOURS_TO_WORK:
                                working_hours_amount = self.__MAX_HOURS_TO_WORK
                        else:
                            working_hours_amount = shift.working_end - shift.working_start
                        hoursByShift = workingDay[working_hours_amount]
                        for hours_amount_to_work in hoursByShift:
                            shifts_by_site[site.__site_id-1].append(Shift(shift_start_time, shift_start_time+hours_amount_to_work))
                            shift_start_time += hours_amount_to_work
        return shifts_by_site

    def getShiftsBySite(self) -> List[Shift]:
        return None

    def getCantVigilantesforSite(self):
        cantNecesaryVigilantesforSite = {}
        indexSite = 1
        for place in self.SitesData:
            cantVigilantByPeriod = []
            sum = 0
            for cantByperiod in place:
                cantVigilantByPeriod.append(cantByperiod)
                sum = sum + cantByperiod
            self.cantVigilantsByPeriod.append(cantVigilantByPeriod)
            cantNecesaryVigilantesforSite[indexSite] = sum
            indexSite += 1
        return cantNecesaryVigilantesforSite

    def get_order_site_by_vigilantes_amount()-> int:
        return None

    def OrderSitesForCantVigilantes(self):
        sites = self.getCantVigilantesforSite()
        sites = sorted(sites.items(), key=operator.itemgetter(1), reverse=True)
        site = []
        for i in sites:
            site.append(int(i[0]))
        self.__order_sites_by_vigilantes_amount = site

    def loadWorkingDay(self) -> Dict[int,List[int]]: 
        return { 1:[1],2:[2],3:[3],4:[4],5:[5],6:[6], 7:[7],8:[8],9:[9],10:[10],11:[11],12:[12],13:[7,6],14:[7,7],15:[8,7],16:[8,8],17:[8,9],20:[10,10],21:[7,7,7],22:[8,7,7],
                      23:[8,8,7],24:[8,8,8]}

    def get_working_day_with_constraints(self, key, site):
        response = self.workingDay[key]
        if self.__workingDay[site-1] != 0:
            response = [self.__workingDay[site-1]]
        return response


    def getSite(self, siteId):
        return self.SitesData[siteId-1]

   