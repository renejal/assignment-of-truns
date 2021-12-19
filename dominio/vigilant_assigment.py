from typing import Dict, List
from dominio.model.site import Site
from dominio.model.vigilant import Vigilant
from dominio.model.shift import Shift
import operator
from services.shifts_generation_service import Shifts_generation_service


class VigilantAssigment:
    # maxShiftDuration: int = 12
    # minShiftDuration: int = 4
    # minBreakDuration: int = 18
    # maxOvertimeWorkHoursPerWeek=12
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


    def __init__(self, vigilantes: List[Vigilant], sites: List[Site], weeks) -> None:
        self.vigilantes = vigilantes
        self.sites = sites
        self.total_weeks = weeks
        self.total_sites = len(sites)
        self.expectec_places_to_look_out_by_vigilants = {}
        self.initProblem()

    def initProblem(self) -> None:
        for vigilant in self.vigilantes:
            vigilant.set_total_hours_worked_by_week(self.total_weeks)
            if vigilant.default_place_to_look_out != self.__DEFAULT_PLACE_TO_LOOK_OUT_FORMAT:
                if vigilant.default_place_to_look_out in self.expectec_places_to_look_out_by_vigilants:
                    self.expectec_places_to_look_out_by_vigilants[vigilant.default_place_to_look_out].append(vigilant.id)
                else:
                    self.expectec_places_to_look_out_by_vigilants[vigilant.default_place_to_look_out] = vigilant.id
        self.shifts_by_sites = Shifts_generation_service().create_shifts_by_site(self.sites,self.total_weeks)
        self.order_sites_by_id_vigilantes_amount = self.sorted_sites_by_vigilant_amount(self.shifts_by_sites)

    def sorted_sites_by_vigilant_amount(self, shifts_by_sites:List[List[Shift]] ):
        vigilantes_needed_by_site = self.get_vigilantes_needed_by_site(shifts_by_sites)
        vigilantes_needed_sorted_by_site = sorted(vigilantes_needed_by_site.items(), key=operator.itemgetter(1), reverse=True)
        order_sites = []
        for i in vigilantes_needed_sorted_by_site:
            order_sites.append(int(i[0]))
        return order_sites

    def get_vigilantes_needed_by_site(self,shifts_by_sites:List[List[Shift]]) -> Dict[int,int]:
        vigilantes_needed_by_site = {}
        for indexSite, site_shifts in enumerate(shifts_by_sites):
            acc = 0
            for shift in site_shifts:
                acc += shift.necesary_vigilantes
            vigilantes_needed_by_site[indexSite + 1] = acc
        return vigilantes_needed_by_site
    
    def get_order_site_by_vigilantes_amount(self, pos: int) -> int:
        return self.get_site(self.order_sites_by_id_vigilantes_amount[pos])

    def get_site(self, site_id:int) -> int:
        return self.sites[site_id-1].id

    def get_shifts_on_site(self, site_id:int) -> List[Shift]:
        return self.shifts_by_sites[site_id-1]


   