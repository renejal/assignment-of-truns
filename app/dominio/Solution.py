import copy
from typing import List
from dominio.model.site import Site
from dominio.model.shift import Shift
from dominio.model.vigilant import Vigilant
from dominio.Component import Component
import random
from dominio.vigilant_assigment import VigilantAssigment
from services.site_schedule_service import Site_schedule_service
from conf.settings import *
from utils.order import Order

class Solution:

    problem = VigilantAssigment
    sites_schedule: List[Component]
    vigilantes_schedule: List[Vigilant] 
    site_schedule_service: Site_schedule_service

    fitness:List[int]
    missing_shifts_fitness: int
    distance_fitness: int
    extra_hours_fitness: int
    assigned_vigilantes_fitness: int
    total_fitness: int

    crowding_distance:int
    dominated: List[int]
    dominate_me: int
    range: int
    id: int
    fitnessToOptimize: str

    def __init__(self, problem: VigilantAssigment):
        self.site_schedule_service = Site_schedule_service(problem)
        self.problem = problem
        self.sites_schedule = [None] * len(problem.sites)
        self.vigilantes_schedule = copy.deepcopy(problem.vigilantes)
        self.__iteration = 0
        self.dominate_me = 0
        self.range = -1
        self.id = 0
        self.crowding_distance = 0
        self.fitnessToOptimize = self.get_fitness_to_optimize()

    def get_fitness_to_optimize(self) -> str:
        objectives = ["missing_shifts","necesary_vigilantes","extra_hours","distance"]
        return random.choices(objectives, weights =(MISSING_SHIFT_PROBABILITY,ASSIGNED_VIGILANTES_PROBABILITY,EXTRA_HOURS_PROBABILITY,DISTANCE_GRASP_PROBABILITY))[0]

    def create_components(self, components_new_amount: int):
        components: List[Component] = []
        site: Site = self.problem.get_order_site_by_vigilantes_amount(self.__iteration)
        shifts: List[Shift] = self.problem.get_shifts_on_site(site.id)
        order_vigilantes_ids_in_site = self.problem.order_sites_by_id_vigilantes_distance[site.id-1]
        order_vigilantes_in_site = []
        expected_vigilantes_in_place = []

        for vigilant_id in order_vigilantes_ids_in_site:
            vigilant = self.vigilantes_schedule[vigilant_id-1]
            if vigilant.is_usuable and vigilant.default_place_to_look_out == -1:
                order_vigilantes_in_site.append(vigilant) 
        
        if site.id in self.problem.expected_places_to_look_out_by_vigilants:
            for vigilant_id in self.problem.expected_places_to_look_out_by_vigilants.get(site.id):
                expected_vigilantes_in_place.append(self.vigilantes_schedule[vigilant_id-1])

        for component in range(components_new_amount):
            component = self.site_schedule_service.get_site_schedule(site.id, copy.deepcopy(shifts),copy.deepcopy(order_vigilantes_in_site),copy.deepcopy(expected_vigilantes_in_place)) #DELETE FOR REAL PROBLEM
            components.append(component)
        return components

    def get_best_components(self, components: List[Component], restricted_components_amount: int):
        for iteration in range(restricted_components_amount):
            swapped = False
            for pos in range(len(components)-1-iteration):
                if(components[pos + 1].get_fitness_by_criteria(self.fitnessToOptimize) < components[pos].get_fitness_by_criteria(self.fitnessToOptimize)):
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
        self.sites_schedule[component.site_id-1] = component
        self.__iteration += 1
        # if component.assigned_Vigilantes. == None:
        #     return
        for vigilant in component.assigned_Vigilantes.values():
            if len(vigilant.sites_to_look_out) > 1:
                for shift in self.vigilantes_schedule[vigilant.id-1].shifts:
                    for updated_shift in vigilant.shifts:
                        if updated_shift.shift.shift_start == shift.shift.shift_start:
                            updated_shift.shift = shift.shift
                            updated_shift = shift
                            break
                for site in vigilant.sites_to_look_out:
                    if site != component.site_id:
                        self.sites_schedule[site-1].assigned_Vigilantes[vigilant.id] = vigilant
            self.vigilantes_schedule[vigilant.id-1] = vigilant

    def is_solution_complete(self):
        if self.__iteration < self.problem.total_sites:
            return True
        self.calculate_fitness()
        return False

    def add_dominate(self, id):
        self.dominated.append(id)
    
    
    def get_random_gen(self, ids_gen_not_avaliable: List[int]) -> Component:
        response = True
        while response:
            gen =self.sites_schedule[random.randint(0,len(self.sites_schedule)-1)]
            if gen.site_id in ids_gen_not_avaliable:
                #"el componente ya esta la lista"
                continue
            return gen
        
    
    def get_best_componente_by_fitnnes(self,fitnessToOptimize,rango_percentage):
        """Obtiene el mejor gen de un rango porsentual de la lista obtenidad ordenada por fitnnes"""
        return  Order.order_sitio_of_objective_value(self.sites_schedule,fitnessToOptimize)
        
    
    def crossing_vigilant(self, id_vigilant_new:int, id_vigilant_exchange: int):
        for gen in self.sites_schedule:
            for vigilant_id in gen.assigned_Vigilantes:
                if vigilant_id== id_vigilant_exchange:
                    gen.assigned_Vigilantes.get(vigilant_id).set_id(id_vigilant_new) 
                elif vigilant_id== id_vigilant_new:
                    gen.assigned_Vigilantes.get(vigilant_id).set_id(id_vigilant_exchange)
            
    def calculate_fitness(self):
        self.missing_shifts_fitness = 0
        self.distance_fitness = 0
        self.extra_hours_fitness = 0
        self.assigned_vigilantes_fitness = 0
        self.total_fitness = 0
        self.fitness = [0,0,0,0]
        for site in self.sites_schedule:
            for shift in site.missing_shifts:
                if shift.necesary_vigilantes != len(shift.assigment_vigilantes):
                    self.missing_shifts_fitness+= MISSING_FITNESS_VALUE*(shift.necesary_vigilantes - len(shift.assigment_vigilantes))
                    self.fitness[0] = self.missing_shifts_fitness
                    self.total_fitness+= MISSING_FITNESS_VALUE*(shift.necesary_vigilantes - len(shift.assigment_vigilantes))
        vigilantes_amount_assigned = 0
        for vigilant in self.vigilantes_schedule:
            for site_to_look_out in vigilant.sites_to_look_out:
                if site_to_look_out != vigilant.default_place_to_look_out and site_to_look_out != vigilant.closet_place:
                    # self.distance_fitness+= vigilant.distances[site_to_look_out-1]    
                    # self.total_fitness+= vigilant.distances[site_to_look_out-1]
                    self.distance_fitness+= DISTANCE_FITNESS_VALUE * vigilant.order_distances.get(site_to_look_out)
                    self.fitness[1] = self.distance_fitness * vigilant.order_distances.get(site_to_look_out)
                    self.total_fitness+= DISTANCE_FITNESS_VALUE  
            for index, hour_by_week in enumerate(vigilant.total_hours_worked_by_week):
                if hour_by_week > 48:
                    self.extra_hours_fitness += EXTRA_HOURS_FITNESS_VALUE * (hour_by_week - 48)
                    self.total_fitness += EXTRA_HOURS_FITNESS_VALUE * (hour_by_week - 48)
                    self.fitness[2] = self.extra_hours_fitness
                if hour_by_week < 48 and hour_by_week > 0:
                    missing_hours = hour_by_week
                    if hour_by_week >= 24:
                        missing_hours = 48 - hour_by_week                        
                    self.assigned_vigilantes_fitness += missing_hours
                    self.total_fitness+=  missing_hours
                    self.fitness[3] = self.assigned_vigilantes_fitness
            if vigilant.is_assigned:
                vigilantes_amount_assigned += 1
        self.assigned_vigilantes_fitness += ASSIGNED_VIGILANTES_FITNESS_VALUE * (vigilantes_amount_assigned - self.problem.expected_vigilantes)
        self.total_fitness += ASSIGNED_VIGILANTES_FITNESS_VALUE * (vigilantes_amount_assigned - self.problem.expected_vigilantes)

    def calculate_assigned_vigilantes_fitness(self):
        count = 0
        for vigilant in self.vigilantes_schedule:
            if vigilant.is_assigned:
                count += 1
        return count - self.problem.expected_vigilantes 