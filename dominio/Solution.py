from typing import List
#from dominio.Shift import Shift
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
from services.generate_site_schedule_service import generate_site_schedule_service
from services.obtain_vigilantes_service import obtain_vigilantes_service
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
        self.__sitesSchedule = [[]]*(self.__problem.total_sites)
        self.vigilantesSchedule = self.__problem.vigilantes.copy()
        self.__iteration = 0
        self.vigilantesForPlaces = [[]]*(self.__problem.total_sites) ##Cuestiar si hay que moverlo al metodo o cambior por acceso al componente

    def create_components(self, components_new_amount):
        components = List[Component]
        site_id = self.__problem.get_order_site_by_vigilantes_amount(self.__iteration)
        shifts = self.__problem.get_shifts_on_site(site_id) 
        possible_vigilantes_to_assign = obtain_vigilantes_service.getPossibleVigilantesToAssign(site_id, shifts)
        for component in range(0, components_new_amount):
            component = Component(site_id, shifts) #Verificar que los shifts no cambien por referencia si no crear copia
            generate_site_schedule_service.getSchedule(component, shifts, copy.deepcopy(possible_vigilantes_to_assign))
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

    def merge_component(self, component):
        for vigilant in component.assignedVigilantes:
            self.vigilantesSchedule[vigilant.id-1] = vigilant
            self.vigilantesForPlaces[component.siteId-1].append(vigilant)
        self.sitesSchedule[component.siteId-1] = component.siteSchedule
        self.missingShiftsBySite[component.siteId-1] = component.missingShfits
        self.__fitness += component.fitness
        self.__iteration += 1

    def is_solution_complete(self):
        if self.__iteration < len(self.__sitesSchedule):
            return True
        #self.missingShiftsFormat(self.missingShiftsBySite)
        return False

    def calculate_fitness(self, solution):
        solution.Fitness = 0
        for site in range(0, len(solution.sitesSchedule)):
            for period in range(0, len(solution.sitesSchedule[site])):
                actualVigilantes = len(solution.sitesSchedule[site][period])
                missingVigilantes = self.__problem.cantVigilantesByPeriod[site][period] - \
                    actualVigilantes
                solution.Fitness += missingVigilantes*10000
        for vigilant in self.vigilantesSchedule:
            for assignedPlace in vigilant.shifts:
                if assignedPlace != 0:
                    # calculate fitness distance
                    if vigilant.expectedPlaceToWatch != assignedPlace:
                        solution.Fitness += 500
                    # calculate work hours
                    for hourWeek in vigilant.HoursWeeks:
                        if hourWeek < 40 and hourWeek != 0:
                            solution.Fitness += 800
                        if hourWeek > 48:
                            solution.Fitness += 300
                    # Calculate preferencias
                    # TODO

    def update_Fitnees(self, objVigilantes: Vigilant, site, newSite,solucion):
        solucion.Fitness -= objVigilantes.distancesBetweenPlacesToWatch[site]
        solucion.Fitness += objVigilantes.distancesBetweenPlacesToWatch[newSite]

    
  
    ##No puede encontrar coneccion
    def getVigilantesForPlaceList(self, vigilantesForPlace):
        listSite = []
        for site in vigilantesForPlace:
            listSite.append(vigilantesForPlace[site])
        return listSite

    

   

    

    

    

    
