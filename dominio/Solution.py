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
from utils import aleatory
from services.site_schedule_service import site_schedule_service
from services.vigilant_assigment_service import Vigilant_assigment_service
#Como se crea un individuo en NSGA-II


class Solution:

    __problem = VigilantAssigment
    __vigilantes: List[Vigilant]
    __sitesSchedule: List[Component]
    __vigilantesSchedule: List[Vigilant] 
    __fitness: List[int]
    vigilantesForPlaces = [] ## cuestionar este atributo

    def __init__(self, problem: VigilantAssigment , Aletory):
        random.seed(Aletory) ## PROBAR SI AFECTA EL ALEATORIO Y SI NO ELIMINARLO
        self.__problem = problem
        self.__vigilantes = problem.vigilantes.copy()
        # self.__sitesSchedule = [[]]*(self.__problem.total_sites)
        self.vigilantesSchedule = self.__problem.vigilantes.copy()
        self.__iteration = 0
        self.vigilantesForPlaces = [[]]*(self.__problem.total_sites) ##Cuestiar si hay que moverlo al metodo o cambior por acceso al componente

    def create_components(self, components_new_amount: int):
        components = List[Component]
        site_id: int = self.__problem.get_order_site_by_vigilantes_amount(self.__iteration)
        shifts: List[Shift] = self.__problem.get_shifts_on_site(site_id)
        # possible_vigilantes_to_assign = Vigilant_assigment_service.get_possible_vigilant_to_assign(site_id)
        for component in range(0, components_new_amount):
            # component = site_schedule_service.get_site_schedule(site_id, shifts, copy.deepcopy(possible_vigilantes_to_assign)) #Verificar que los shifts no cambien por referencia si no crear copia
            component = site_schedule_service.get_site_schedule(site_id, shifts, self.vigilantesSchedule.copy()) #Verificar que los shifts no cambien por referencia si no crear copia
            component.calculate_fitness()
            components.append(component)
        return components

    def get_best_components(self, components, cantRestrictedComponets):
        # Fitness de la solucion
        for iteration in range(0, cantRestrictedComponets):
            swapped = False
            for pos in range(0, len(components)-1-iteration):
                if(components[pos + 1].fitness < components[pos].fitness):
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
        for vigilant in component.__assigned_Vigilantes:
            self.vigilantesSchedule[vigilant.id-1] = vigilant
            self.vigilantesForPlaces[component.siteId-1].append(vigilant)        
        self.__sitesSchedule.append(component)
        # self.__fitness += component.fitness
        self.__iteration += 1

    def is_solution_complete(self):
        if self.__iteration < len(self.__problem.total_sites):
            return True
        #self.missingShiftsFormat(self.missingShiftsBySite)
        return False

    def update_Fitnees(self, objVigilantes: Vigilant, site, newSite,solucion):
        solucion.Fitness -= objVigilantes.distancesBetweenPlacesToWatch[site]
        solucion.Fitness += objVigilantes.distancesBetweenPlacesToWatch[newSite]

    

   

    

    

    

    
