from typing import List
from dominio.Shift import Shift
from dominio.Vigilant import Vigilant
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
from services.obtain_vigilants_service import obtain_vigilants_service
#Como se crea un individuo en NSGA-II


class Solution:

    __problem = VigilantAssigment
    __vigilants: List[Vigilant]
    __sitesSchedule: List[Component]
    __vigilantsSchedule: List[Vigilant] 
    __fitness: list[int]
    vigilantsForPlaces = [] ## cuestionar este atributo

    def __init__(self, problem: VigilantAssigment , Aletory):
        random.seed(Aletory) ## PROBAR SI AFECTA EL ALEATORIO Y SI NO ELIMINARLO
        self.__problem = problem
        self.__vigilants = self.__problem.vigilantes.copy()
        self.__sitesSchedule = [[]]*(self.__problem.totalPlaces)
        self.vigilantsSchedule = self.__problem.vigilantes.copy()
        self.__iteration = 0
        self.vigilantsForPlaces = [[]]*(self.__problem.totalPlaces) ##Cuestiar si hay que moverlo al metodo o cambior por acceso al componente

    def create_components(self, components_new_amount):
        components = List[Component]
        site_id = self.__problem.get_order_site_by_vigilants_amount(self.__iteration)
        shifts = self.__problem.get_shifts_by_site(site_id) 
        possible_vigilants_to_assign = obtain_vigilants_service.getPossibleVigilantsToAssign(site_id, shifts)
        for component in range(0, components_new_amount):
            component = Component(site_id, shifts) #Verificar que los shifts no cambien por referencia si no crear copia
            generate_site_schedule_service.getSchedule(component, shifts, copy.deepcopy(possible_vigilants_to_assign))
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
        for vigilant in component.assignedVigilants:
            self.vigilantsSchedule[vigilant.id-1] = vigilant
            self.vigilantsForPlaces[component.siteId-1].append(vigilant)
        self.sitesSchedule[component.siteId-1] = component.siteSchedule
        self.missingShiftsBySite[component.siteId-1] = component.missingShfits
        self.__fitness += component.fitness
        self.__iteration += 1

    def is_solution_complete(self):
        if self.__iteration < len(self.sitesSchedule):
            return True
        #self.missingShiftsFormat(self.missingShiftsBySite)
        return False

    def calculate_fitness(self, solution):
        solution.Fitness = 0
        for site in range(0, len(solution.sitesSchedule)):
            for period in range(0, len(solution.sitesSchedule[site])):
                actualVigilants = len(solution.sitesSchedule[site][period])
                missingVigilants = self.__problem.cantVigilantsByPeriod[site][period] - \
                    actualVigilants
                solution.Fitness += missingVigilants*10000
        for vigilant in self.vigilantsSchedule:
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

    def update_Fitnees(self, objVigilants: Vigilant, site, newSite,solucion):
        solucion.Fitness -= objVigilants.distancesBetweenPlacesToWatch[site]
        solucion.Fitness += objVigilants.distancesBetweenPlacesToWatch[newSite]

    
  
    ##No puede encontrar coneccion
    def getVigilantsForPlaceList(self, vigilantsForPlace):
        listSite = []
        for site in vigilantsForPlace:
            listSite.append(vigilantsForPlace[site])
        return listSite

    

   

    

    

    

    
