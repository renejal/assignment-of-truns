from typing import List
from dominio.Solution import Solution
from dominio.model.shift import Shift
from dominio.model.vigilant import Vigilant
from services.vigilant_assigment_service import Vigilant_assigment_service
from utils import aleatory

class Tweak_service:

    vigilant_assigment_service: Vigilant_assigment_service = Vigilant_assigment_service(None)


    def Tweak(self, solution: Solution):
        solution = self.missing_shifts_tweak(solution)
        solution.calculate_fitness()
        #solution = self.tweakVigilants(solution)
        #self.calculateFitness(solution)
        return solution
    
    def get_vigilantes_with_missing_hours(self, vigilantes: List [Vigilant]) -> List[Vigilant]:
        vigilantes_with_missing_hours: List[Vigilant] = []
        for vigilant in vigilantes:
            for hours_worked_on_week in vigilant.total_hours_worked_by_week:
                if hours_worked_on_week < 40 and vigilant not in vigilantes_with_missing_hours:
                    vigilantes_with_missing_hours.append(vigilant)
        return vigilantes_with_missing_hours

    def assign_vigilantes_on_missing_shifts(self, vigilantes:List[Vigilant], site_id: int, shifts: List[Shift]) :
        #Select ramdom?
        assigned_vigilantes_in_actual_shift: List[int] = []
        for shift in shifts:
            assigned_vigilantes_in_actual_shift.clear()
            for iteration in range(shift.necesary_vigilantes - len(shift.assigment_vigilantes)):
                for vigilant in vigilantes:    
                    if vigilant is not assigned_vigilantes_in_actual_shift and self.vigilant_assigment_service.is_vigilant_avaible(vigilant, shift):
                        vigilant.assign_shift(shift, site_id)
                        shift.add_vigilant(vigilant.id)
                        assigned_vigilantes_in_actual_shift.append(vigilant.id)
                        if self.vigilant_assigment_service.check_if_vigilant_has_missing_hours(vigilant)!= True:
                            vigilantes.remove(vigilant)
                        break
            if shift.necesary_vigilantes == len(shift.assigment_vigilantes):
                shifts.remove(shift)
        
    def assign_extra_hours_on_vigilantes(self, vigilantes:List[Vigilant], site_id: int, shifts: List[Shift]):
        self.vigilant_assigment_service._MAXIMUM_WORKING_AMOUNT_HOURS_BY_WEEK = 56
        self.assign_vigilantes_on_missing_shifts(vigilantes,site_id, shifts)
        self.vigilant_assigment_service._MAXIMUM_WORKING_AMOUNT_HOURS_BY_WEEK = 48

    def get_vigilantes_from_other_sites(self, vigilantes: List[Vigilant], assigned_vigilants_on_site: List[Vigilant] ):
        vigilantes_from_other_sites: List[Vigilant] = []
        for vigilant in vigilantes:
            for assigned_vigilant_in_site in assigned_vigilants_on_site:
                if assigned_vigilant_in_site.id == vigilant.id:
                    break
            else:    
                vigilantes_from_other_sites.append(vigilant)     
        return vigilantes_from_other_sites

    def missing_shifts_tweak(self, solution: Solution) -> Solution:
        vigilantes_with_missing_hours: List[Vigilant] = self.get_vigilantes_with_missing_hours(solution.vigilantes_schedule)
        #Asignar a los turnos los vigilantes que tienen menos de 40 horas en el mismo sitio
        for site in solution.sites_schedule:
             vigilantes = [x for x in vigilantes_with_missing_hours if site.site_id in x.sites_to_look_out]
             self.assign_vigilantes_on_missing_shifts(vigilantes,site.site_id,site.missing_shifts)
        #Asignar horas extras a los vigilantes en el mismo sitio
        for site in solution.sites_schedule:
            vigilantes = [x for x in site.assigned_Vigilantes if solution.vigilantes_schedule[x.id-1]]
            self.assign_extra_hours_on_vigilantes(site.assigned_Vigilantes, site.site_id, site.missing_shifts)
        #Asignar a los turnos los vigilantes que tienen menos de 40 horas en algun otro sitio
        for site in solution.sites_schedule:            
            vigilantes = self.get_vigilantes_from_other_sites( solution.vigilantes_schedule, site.assigned_Vigilantes)
            self.assign_vigilantes_on_missing_shifts(vigilantes,site.site_id,site.missing_shifts)
        #quitarle horas a alguien que tenga 48 horas y asignar uno que tenga menos horas
        #Asignar horas extras a los vigilantes en el mismo sitio
        for site in solution.sites_schedule:
            vigilantes = self.get_vigilantes_from_other_sites( solution.vigilantes_schedule, site.assigned_Vigilantes)    
            self.assign_extra_hours_on_vigilantes(vigilantes, site.site_id, site.missing_shifts)
        return solution

    def tweakVigilants(self, solucion):
        if self.is_empty(solucion.vigilantesForPlaces):
            listSite = aleatory.get_aleatory(0, len(solucion.vigilantesForPlaces) - 1, 2)
            vigilantOne = aleatory.get_aleatory(0, len(solucion.vigilantesForPlaces[listSite[0]]), 1)
            vigilantTwo = aleatory.get_aleatory(0, len(solucion.vigilantesForPlaces[listSite[1]]), 1)
            self.toExchageVigilants(listSite[0], vigilantOne[0], listSite[1], vigilantTwo[0], solucion)
        return solucion
 

    def toExchageVigilants(self, parIdSiteOne, parIdVigilantOne, parIdSiteTwo, parIdVigilantsTwo,solucion):
        '''
        to Exchage vigilantes between sites
        :param parSiteOne: site one select ramdoly
        :param parVigilantOne: vigilant one select the site one ramdoly
        :param parSiteTwo:
        :param parVigilantsTwo:
        :return: None
        '''
        try:
            objVigilantOne = solucion.vigilantesForPlaces.get(parIdSiteOne)[
                parIdVigilantOne]
            objVigilantTwo = solucion.vigilantesForPlaces.get(parIdSiteOne)[
                parIdVigilantOne]
            self.updateFitnees(objVigilantOne, parIdSiteOne,
                               parIdSiteTwo, solucion)
            self.updateFitnees(objVigilantTwo, parIdSiteTwo,
                               parIdSiteOne, solucion)
            temVigilanOne = solucion.vigilantesForPlaces.get(parIdSiteOne)[
                parIdVigilantOne]
            solucion.vigilantesForPlaces.get(parIdSiteOne)[
                parIdVigilantOne] = solucion.vigilantesForPlaces.get(parIdSiteTwo)[parIdVigilantsTwo]
            solucion.vigilantesForPlaces.get(
                parIdSiteTwo)[parIdVigilantsTwo] = temVigilanOne
        except:
            print("exception")
    
    def getAleatory(self, parInit, parEnd, parNumber):
        '''
        generate n number aleatory between  nunber init and number end
        :param init: number init
        :param end: number end
        :param number: quantity the number aleatory
        :return: list number aleatory
        '''
        k = 0
        listAleatory = []
        while True:
            if parNumber > k:
                numAleatory = random.randint(parInit, parEnd)
                if numAleatory not in listAleatory:
                    listAleatory.append(numAleatory)
                    k = k+1
            else:
                break
        return listAleatory
    
    def is_empty(self, list):
        varResult = True
        for i in list:
            if i is None:
                varResult = False
                break
        return varResult