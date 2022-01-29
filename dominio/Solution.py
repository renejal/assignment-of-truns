import copy 
from typing import List
from dominio.model.shift import Shift
from dominio.model.vigilant import Vigilant
from dominio.Component import Component
import random
from dominio.vigilant_assigment import VigilantAssigment
from services.site_schedule_service import Site_schedule_service
from conf.settings import MISSING_FITNESS_VALUE,DISTANCE_FITNESS_VALUE,EXTRA_HOURS_FITNESS_VALUE,ASSIGNED_VIGILANTES_FITNESS_VALUE

class Solution:

    problem = VigilantAssigment
    sites_schedule: List[Component]
    vigilantes_schedule: List[Vigilant] 
    site_schedule_service: Site_schedule_service
    missing_shifts_fitness: int
    distance_fitness: int
    extra_hours_fitness: int
    assigned_vigilantes_fitness: int
    total_fitness: int
    id: int

    def __init__(self, problem: VigilantAssigment , Aletory):
        self.site_schedule_service = Site_schedule_service(problem)
        self.problem = problem
        self.sites_schedule = []
        self.vigilantes_schedule = problem.vigilantes.copy()
        self.__iteration = 0
        #self.vigilantesForPlaces = [[]]*(self.__problem.total_sites) ##Cuestiar si hay que moverlo al metodo o cambior por acceso al componente

    def create_components(self, components_new_amount: int):
        components: List[Component] = []
        site_id: int = self.problem.get_order_site_by_vigilantes_amount(self.__iteration)
        shifts: List[Shift] = self.problem.get_shifts_on_site(site_id)
        for component in range(components_new_amount):
            component = self.site_schedule_service.get_site_schedule(site_id, copy.deepcopy(shifts),copy.deepcopy(self.vigilantes_schedule))
            components.append(component)
        return components

    def get_best_components(self, components: List[Component], restricted_components_amount: int):
        for iteration in range(restricted_components_amount):
            swapped = False
            for pos in range(len(components)-1-iteration):
                if(components[pos + 1].total_fitness < components[pos].total_fitness):
                    aux = components[pos]
                    components[pos] = components[pos+1]
                    components[pos + 1] = aux
                    swapped = True
            if swapped == False:
                break
            pass
        restrictedList = components[:restricted_components_amount]
        return restrictedList[random.randint(0, restricted_components_amount-1)]

    def merge_component(self, component : Component):
        self.sites_schedule.append(component)
        self.__iteration += 1
        if component.assigned_Vigilantes == None:
            return
        for vigilant in component.assigned_Vigilantes:
            self.vigilantes_schedule[vigilant.id-1] = vigilant

    def is_solution_complete(self):
        if self.__iteration < self.problem.total_sites:
            return True
        self.calculate_fitness()
        return False

    def calculate_fitness(self):
        self.missing_shifts_fitness = 0
        self.distance_fitness = 0
        self.extra_hours_fitness = 0
        self.assigned_vigilantes_fitness = 0
        self.total_fitness = 0
        for site in self.sites_schedule:
            for shift in site.missing_shifts:
                if shift.necesary_vigilantes != len(shift.assigment_vigilantes):
                    self.missing_shifts_fitness+= MISSING_FITNESS_VALUE*(shift.necesary_vigilantes - len(shift.assigment_vigilantes))
                    self.total_fitness+= MISSING_FITNESS_VALUE*(shift.necesary_vigilantes - len(shift.assigment_vigilantes))
        for vigilant in self.vigilantes_schedule:
            for site_to_look_out in vigilant.sites_to_look_out:
                if site_to_look_out != vigilant.default_place_to_look_out and site_to_look_out != vigilant.closet_place:
                    self.distance_fitness+= DISTANCE_FITNESS_VALUE    
                    self.total_fitness+= DISTANCE_FITNESS_VALUE  
            for index, hour_by_week in enumerate(vigilant.total_hours_worked_by_week):
                if hour_by_week > 48:
                    self.extra_hours_fitness += EXTRA_HOURS_FITNESS_VALUE
                    self.total_fitness += EXTRA_HOURS_FITNESS_VALUE
                # if index+1 == len(vigilant.total_hours_worked_by_week):
                #     break
                if hour_by_week < 40 and hour_by_week > 0:
                    self.assigned_vigilantes_fitness += ASSIGNED_VIGILANTES_FITNESS_VALUE
                    self.total_fitness+= ASSIGNED_VIGILANTES_FITNESS_VALUE  




   

    

    

    

    
