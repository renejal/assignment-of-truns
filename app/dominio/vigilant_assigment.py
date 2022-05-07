import operator
from traceback import print_tb
from typing import Dict, List
from dominio.model.site import Site
from dominio.model.vigilant import Vigilant
from dominio.model.shift import Shift
from services.shifts_generation_service import Shifts_generation_service
from conf.settings import MAX_TOTAL_WEEKS

class VigilantAssigment:
    
    vigilantes: List[Vigilant]
    sites: List[Site]
    total_vigilantes: int
    total_sites: int
    expected_places_to_look_out_by_vigilants: Dict[int, List[int]]
    order_sites_by_id_vigilantes_amount: List[int]
    order_sites_by_id_vigilantes_distance: List[List[int]]
    shifts_by_sites: List[List[Shift]]

    DEFAULT_PLACE_TO_LOOK_OUT_FORMAT: int = -1
    MAX_TOTAL_WEEKS = MAX_TOTAL_WEEKS

    def __init__(self, vigilantes: List[Vigilant], sites: List[Site]) -> None:
        self.vigilantes = vigilantes
        self.sites = sites
        self.total_sites = len(sites)
        self.expected_places_to_look_out_by_vigilants = {}
        self.order_sites_by_id_vigilantes_distance = []
        self.initProblem()

    def initProblem(self) -> None:
        sitesDict = self.mapSites(self.sites)
        print("sitesdict", sitesDict)
        for index, vigilant in enumerate(self.vigilantes):
            vigilant.set_id(index+1)
            if vigilant.default_place_to_look_out!= -1:
                print(vigilant.default_place_to_look_out)
                print(sitesDict[vigilant.default_place_to_look_out])
                vigilant.default_place_to_look_out = sitesDict[vigilant.default_place_to_look_out]
            vigilant.closet_place = sitesDict[vigilant.closet_place]
            vigilant.set_total_hours_worked_by_week(self.MAX_TOTAL_WEEKS)
            if vigilant.default_place_to_look_out != self.DEFAULT_PLACE_TO_LOOK_OUT_FORMAT:
                if vigilant.default_place_to_look_out in self.expected_places_to_look_out_by_vigilants:
                    self.expected_places_to_look_out_by_vigilants[vigilant.default_place_to_look_out].append(vigilant.id)
                else:
                    self.expected_places_to_look_out_by_vigilants[vigilant.default_place_to_look_out] = [vigilant.id]
        self.shifts_by_sites = Shifts_generation_service().create_shifts_by_site(self.sites)
        self.order_sites_by_id_vigilantes_amount = self.sorted_sites_by_vigilant_amount(self.shifts_by_sites)
        self.order_sites_by_id_vigilantes_distance = self.order_sites_by_vigilantes_distance(self.vigilantes, self.total_sites)

    def mapSites(self, sites: List[Site]):
        sitesDict: Dict[str, int] = {}
        for site in sites:
            sitesDict[site.description] = site.id
        return sitesDict

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

    def order_sites_by_vigilantes_distance(self, vigilants: List[Vigilant], total_sites: int) -> None:
        print("total_sites",total_sites)
        order_sites_by_id_vigilantes_distance = []
        for site in range(total_sites):
            order_site_by_vigilantes_distance = self.order_site_by_vigilantes_distance(vigilants,site)
            order_sites_by_id_vigilantes_distance.append(order_site_by_vigilantes_distance)
        return order_sites_by_id_vigilantes_distance

    def order_site_by_vigilantes_distance(self,vigilantes: List[Vigilant], site_id: int) -> Dict:
        print(site_id)
        dict_order_the_vigilants_for_distance: Dict[int, int] = {}
        for vigilant in vigilantes:
            dict_order_the_vigilants_for_distance[vigilant.id] = vigilant.distances[site_id-1]
        dict_order_the_vigilants_for_distance = sorted(dict_order_the_vigilants_for_distance.items(), key=operator.itemgetter(1))
        order_vigilant_by_site = []
        for site in dict_order_the_vigilants_for_distance:
            order_vigilant_by_site.append(int(site[0]))
        return order_vigilant_by_site
   