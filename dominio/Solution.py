from typing import List
from dominio.model.shift import Shift
from dominio.model.vigilant import Vigilant
from dominio.Component import Component
from random import random
import random
import math
import numpy as np
from dominio.Algorithm import Algorithm
from dominio.vigilant_assigment import VigilantAssigment
import copy 
import collections
from services.vigilant_assigment_service import Vigilant_assigment_service
from utils import aleatory
from services.site_schedule_service import Site_schedule_service
#Como se crea un individuo en NSGA-II


class Solution:

    problem = VigilantAssigment
    sites_schedule: List[Component]
    vigilantes_schedule: List[Vigilant] 
    site_schedule_service: Site_schedule_service
    missing_shifts_fitness: int = 0
    distance_fitness: int = 0
    extra_hours_fitness: int = 0
    assigned_vigilantes_fitness: int = 0
    total_fitness: int = 0

    def __init__(self, problem: VigilantAssigment , Aletory):
        random.seed(Aletory) ## PROBAR SI AFECTA EL ALEATORIO Y SI NO ELIMINARLO
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
        for component in range(0, components_new_amount):
            component = self.site_schedule_service.get_site_schedule(site_id, copy.deepcopy(shifts),copy.deepcopy(self.vigilantes_schedule)) #Verificar que los shifts no cambien por referencia si no crear copia
            components.append(component)
        return components

    def get_best_components(self, components: List[Component], cantRestrictedComponets: int):
        for iteration in range(cantRestrictedComponets):
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
        restrictedList = components[:cantRestrictedComponets]
        return restrictedList[random.randint(0, cantRestrictedComponets-1)]

    def merge_component(self, component : Component):
        self.sites_schedule.append(component)
        self.missing_shifts_fitness += component.missing_shifts_fitness
        self.distance_fitness += component.distance_fitness
        self.assigned_vigilantes_fitness += component.assigned_vigilantes_fitness
        self.extra_hours_fitness += component.extra_hours_fitness
        self.total_fitness += component.total_fitness
        self.__iteration += 1
        if component.assigned_Vigilantes == None:
            return
        for vigilant in component.assigned_Vigilantes:
            self.vigilantes_schedule[vigilant.id-1] = vigilant
       #     self.vigilantesForPlaces[component.siteId-1].append(vigilant)        

    def is_solution_complete(self):
        if self.__iteration < self.problem.total_sites:
            return True
        #self.missingShiftsFormat(self.missingShiftsBySite)
        return False

    def update_Fitnees(self, objVigilantes: Vigilant, site, newSite,solucion):
        solucion.Fitness -= objVigilantes.distancesBetweenPlacesToWatch[site]
        solucion.Fitness += objVigilantes.distancesBetweenPlacesToWatch[newSite]

    

   

    

    

    

    
