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
    expected_places_to_look_out_by_vigilants: Dict[int, List[int]]
    order_sites_by_id_vigilantes_amount: List[int]
    order_sites_by_id_vigilantes_distance: List[List[int]]
    shifts_by_sites: List[List[Shift]]

    last_week_is_not_complete: bool = False

    __DEFAULT_PLACE_TO_LOOK_OUT_FORMAT: int = -1
    max_total_weeks = 2

    def __init__(self, vigilantes: List[Vigilant], sites: List[Site]) -> None:
        self.vigilantes = vigilantes
        self.sites = sites
        self.total_sites = len(sites)
        self.expected_places_to_look_out_by_vigilants = {}
        self.order_sites_by_id_vigilantes_distance = []
        self.initProblem()

    def initProblem(self) -> None:
        for vigilant in self.vigilantes:
            vigilant.set_total_hours_worked_by_week(self.max_total_weeks)
            if vigilant.default_place_to_look_out != self.__DEFAULT_PLACE_TO_LOOK_OUT_FORMAT:
                if vigilant.default_place_to_look_out in self.expected_places_to_look_out_by_vigilants:
                    self.expected_places_to_look_out_by_vigilants[vigilant.default_place_to_look_out].append(vigilant.id)
                else:
                    self.expected_places_to_look_out_by_vigilants[vigilant.default_place_to_look_out] = [vigilant.id]
        self.shifts_by_sites = Shifts_generation_service().create_shifts_by_site(self.sites)
        self.order_sites_by_id_vigilantes_amount = self.sorted_sites_by_vigilant_amount(self.shifts_by_sites)
        self.order_sites_by_id_vigilantes_distance = self.order_sites_by_vigilantes_distance(self.vigilantes, self.total_sites)

    def sorted_sites_by_vigilant_amount(self, shifts_by_sites:List[List[Shift]] ):
        vigilantes_needed_by_site = self.get_vigilantes_needed_by_site(shifts_by_sites)
        vigilantes_needed_sorted_by_site = sorted(vigilantes_needed_by_site.items(), key=operator.itemgetter(1), reverse=True)
        order_sites = []
        for site in vigilantes_needed_sorted_by_site:
            order_sites.append(int(site[0]))
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

    def order_sites_by_vigilantes_distance(self,vigilants: List[Vigilant], total_sites: int) -> None:
        order_sites_by_id_vigilantes_distance = []
        for site in range(total_sites):
            order_site_by_vigilantes_distance = self.order_site_by_vigilantes_distance(vigilants,site)
            order_sites_by_id_vigilantes_distance.append(order_site_by_vigilantes_distance)
        return order_sites_by_id_vigilantes_distance

    def order_site_by_vigilantes_distance(self,vigilantes: List[Vigilant], site_id: int) -> Dict:
        dict_order_the_vigilants_for_distance: Dict[int, int] = {}
        for vigilant in vigilantes:
            dict_order_the_vigilants_for_distance[vigilant.id] = vigilant.distances[site_id-1]
        dict_order_the_vigilants_for_distance = sorted(dict_order_the_vigilants_for_distance.items(), key=operator.itemgetter(1))
        order_vigilant_by_site = []
        for site in dict_order_the_vigilants_for_distance:
            order_vigilant_by_site.append(int(site[0]))
        return order_vigilant_by_site
   