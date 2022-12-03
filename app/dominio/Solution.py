import copy
import random
from conf import settings
from conf.settings import *
from utils.order import Order
from typing import List
from dominio.model.site import Site
from dominio.model.shift import Shift
from dominio.model.vigilant import Vigilant
from dominio.Component import Component
from dominio.model.shift import Shift
from dominio.model.vigilant import Vigilant
from dominio.Component import Component
from dominio.vigilant_assigment import VigilantAssigment
from services.site_schedule_service import Site_schedule_service

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
            # if vigilant.is_usuable and vigilant.default_place_to_look_out == -1:
            #     order_vigilantes_in_site.append(vigilant) 
            if vigilant.default_place_to_look_out == -1:
                order_vigilantes_in_site.append(vigilant) 
        
        if site.id in self.problem.expected_places_to_look_out_by_vigilants:
            for vigilant_id in self.problem.expected_places_to_look_out_by_vigilants.get(site.id):
                expected_vigilantes_in_place.append(self.vigilantes_schedule[vigilant_id-1])

        for component in range(components_new_amount):
            component = self.site_schedule_service.get_site_schedule(site.id, copy.deepcopy(shifts),copy.deepcopy(order_vigilantes_in_site),copy.deepcopy(expected_vigilantes_in_place))
            components.append(component)
        return components
    def add_vigilant(self, gen_bad: Component, vigilant_best: Vigilant):
        # obtiene vigilant bad de la solucion actual
        vigilant_bad = self.get_vigilant(vigilant_best.id)
        if vigilant_bad and vigilant_best:
            gen_bad.crossing_shift(vigilant_bad, vigilant_best)
        
    def crossing_gen(self, gen_bad: Component, gen_best: Component):
        list_best_crossing_vigilant = self.get_crossing_vigilant_avaliable(copy.deepcopy(gen_bad), copy.deepcopy(gen_best))
        while list_best_crossing_vigilant:
            vigilants = list_best_crossing_vigilant.pop(0)
            if vigilants[1] == "new vigilant":
                self.add_vigilant(gen_bad, self.get_vigilant(vigilants[0]))
                # gen_bad.add_vigilant(vigilants[0])
            elif vigilants[1] == "delete vigilant":
                gen_bad.delete_vigilant(vigilants[0])
            elif vigilants[1] and vigilants[0]:
                gen_bad.crossing_shift(self.get_vigilant(vigilants[0]), gen_best.assigned_Vigilantes.get(vigilants[1]))
        gen_bad.calculate_inicial_fitness()
    


    def get_crossing_vigilant_avaliable(self, gen_bad: Component, gen_best: Component):
        # obtiene los vigilantes en communt
        vigilants_commont = [vigilant.id for vigilant in gen_best.assigned_Vigilantes.values() if gen_bad.assigned_Vigilantes.get(vigilant.id)]
        # obtiene los vigilantes best
        vigilants_best = [vigilant.id for vigilant in gen_best.assigned_Vigilantes.values()]
        # obtiene los vigilantes bad
        vigilants_bad = [vigilant.id for vigilant in gen_bad.assigned_Vigilantes.values()]
        # otiene los vigilantes no encomun de best
        vigilants_best = list(set(vigilants_best)-set(vigilants_commont))
        # otiene los vigilantes no encomun de bad
        vigilants_bad = list(set(vigilants_bad)-set(vigilants_commont))
        list_result = []
        # asignar parega en comunt para lita resultante
        for vigilant_commont in vigilants_commont:
            list_result.append((vigilant_commont, vigilant_commont))
        # asignar parega en comunt para lita resultante
        while True:
            if vigilants_bad and vigilants_best:
                # los dos tiene vigilantes diponibles, se asignan las pareja
                list_result.append((vigilants_bad.pop(0), vigilants_best.pop(0)))
            elif vigilants_best and not vigilants_bad:
                # el vigilantes bad no tiene vigilants disponible, se asigna etiqueta nuevo vigilante
                # para mantener la integrida en el numero de vigilantes de la solucion best
                list_result.append((vigilants_best.pop(0), "new vigilant"))
            elif not vigilants_best and vigilants_bad:
                # el vigilantes best no tiene vigilants y vigilant bad si tiene, esto quiere decier
                # que se debe quietar resto de vigilantes de la solucion bad 
                list_result.append((vigilants_bad.pop(0), "delete vigilant"))
            elif not vigilants_bad and not vigilants_best:
                # si esta vacio termina la iteracion
                break
        return list_result
        # asignar parega en comunt para lita resultante
        
    def get_vigilant(self, id):
        for vigilant in self.vigilantes_schedule:
            if vigilant.id == id:
                return vigilant
       
    def to_exchange_vigilant(self, gen_best: Component, gen_bad_temp: Component):
        """intercambi el id del vigilant por un nuevo new_id_vigilant del gen por parametro"""
        vigilants_best = gen_best.assigned_Vigilantes
        vigilants_bad = gen_bad_temp.assigned_Vigilantes
        for vigilant_best_id, vigilant_bad_id in zip(vigilants_best, vigilants_bad):
            if vigilants_best.get(vigilant_bad_id): # busca si el vigilante ya se encuentra en el gen si no lo encuentra hace el cambio
                continue
            vigilants_best[vigilant_bad_id] = copy.deepcopy(vigilants_best[vigilant_best_id])
            vigilants_best[vigilant_bad_id].id = vigilant_bad_id
            del vigilants_best[vigilant_best_id]
        
    def get_simility_vigiliant(gen_one: Component, gen_two: Component):
        # sabe que critieros ees bueno tener para inter
        """obtener un reporte de similitud de los vigilantes determinar la mejor asinacion posible"""
        vigilants_one = gen_one.assigned_Vigilantes
        vigilants_two = gen_two.assigned_Vigilantes
        for vigilant_one in vigilants_one.values():
            for vigilant_two in vigilants_two.values():
                pass
            
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
        
    def get_gen(self, id):
        for gen in self.sites_schedule:
            if gen.site_id == id:
                return gen
        raise(f"no se encontro gen con id {id}")


    def get_bad_by_fitnnes(self, fitness_to_optimeze) -> Component:
        """_summary_: obtiene el gen con peor fitnnes de la solucion

        Args:
            fitness_to_optimeze (_type_): _description_

        Returns:
            _type_: _description_
        """
        # ordenar la solucion por fitnes posicion
        gens = Order.order_sitio_of_objective_value(self.sites_schedule,fitness_to_optimeze)
        gens = Order.list_restricted(gens,1,settings.NUM_PARENTS_OF_ORDERED_POPULATION)
        if gens:
            return self.get_gen(gens[0].site_id)
        else:
            return None

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
            for shift in site.site_schedule:
                if shift.necesary_vigilantes != len(shift.assigment_vigilantes):
                    self.missing_shifts_fitness+= MISSING_FITNESS_VALUE*(abs(shift.necesary_vigilantes - len(shift.assigment_vigilantes)))
                    self.total_fitness+= MISSING_FITNESS_VALUE*(abs(shift.necesary_vigilantes - len(shift.assigment_vigilantes)))
                    self.fitness[0] = self.missing_shifts_fitness
        vigilantes_amount_assigned = 0
        for vigilant in self.vigilantes_schedule:
            for site_to_look_out in vigilant.sites_to_look_out:
                # if site_to_look_out != vigilant.default_place_to_look_out and site_to_look_out != vigilant.closet_place:
                    self.distance_fitness+= DISTANCE_FITNESS_VALUE * vigilant.distances[site_to_look_out - 1]
                    self.total_fitness+= DISTANCE_FITNESS_VALUE * vigilant.distances[site_to_look_out - 1]
                    self.fitness[1] = self.distance_fitness
            for index, hour_by_week in enumerate(vigilant.total_hours_worked_by_week):
                if CALCULATE_HOURS_FITNESS:
                    if hour_by_week > MAXIMUM_WORKING_AMOUNT_HOURS_BY_WEEK:
                        self.extra_hours_fitness += EXTRA_HOURS_FITNESS_VALUE * (hour_by_week - MAXIMUM_WORKING_AMOUNT_HOURS_BY_WEEK)
                        self.total_fitness += EXTRA_HOURS_FITNESS_VALUE * (hour_by_week - MAXIMUM_WORKING_AMOUNT_HOURS_BY_WEEK)
                        self.fitness[2] = self.extra_hours_fitness
                if hour_by_week < MAXIMUM_WORKING_AMOUNT_HOURS_BY_WEEK and hour_by_week > 0:
                    missing_hours = MAXIMUM_WORKING_AMOUNT_HOURS_BY_WEEK - hour_by_week
                    # if hour_by_week >= MAXIMUM_WORKING_AMOUNT_HOURS_BY_WEEK/2:
                    #     missing_hours = MAXIMUM_WORKING_AMOUNT_HOURS_BY_WEEK - hour_by_week                        
                    self.assigned_vigilantes_fitness += missing_hours
                    self.total_fitness+=  missing_hours
                    self.fitness[3] = self.assigned_vigilantes_fitness
            if vigilant.is_assigned:
                vigilantes_amount_assigned += 1
        self.assigned_vigilantes_fitness += ASSIGNED_VIGILANTES_FITNESS_VALUE * vigilantes_amount_assigned
        self.total_fitness += ASSIGNED_VIGILANTES_FITNESS_VALUE * vigilantes_amount_assigned
        self.fitness[3] = self.assigned_vigilantes_fitness

    def calculate_assigned_vigilantes_fitness(self):
        count = 0
        for vigilant in self.vigilantes_schedule:
            if vigilant.is_assigned:
                count += 1
        horasExtras = self.fitness[3] - (count * ASSIGNED_VIGILANTES_FITNESS_VALUE)
        return count + horasExtras
    