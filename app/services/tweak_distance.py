import copy
from pickle import NONE
import random
from typing import List
from conf import settings
from conf.settings import STOP_GRASP_TWEAK
from dominio.Component import Component
from dominio.Solution import Solution
from dominio.model.shift_place import Shift_place
from dominio.model.vigilant import Vigilant


class Tweak_distance():
    #Cuestianar si cambiar de lugar un vigilante que ya se encuentra tabranajando en su sitio mas cernano?
    #tirar ramdon tambien al ver con cual vigilante cambiar?
    def tweak_distance(self, solution: Solution):
        vigilantes_with_wrong_assigned_place: List[List[Vigilant]] = self.get_vigilantes_with_wrong_assigned_place(solution.vigilantes_schedule)
        vigilantes_with_one_wrong_assigned_place = vigilantes_with_wrong_assigned_place[0]
        #Case solo pertenecen a un sitio
        if self.change_place_vigilantes_assigned_to_one_place(solution,vigilantes_with_one_wrong_assigned_place):
            if STOP_GRASP_TWEAK:
                return solution
        #Case pertenecen a varios sitios
        vigilantes_with_assigned_place_and_wrong_assigned_places = vigilantes_with_wrong_assigned_place[1]
        random.shuffle(vigilantes_with_assigned_place_and_wrong_assigned_places)
        index = 0
        while index < len(vigilantes_with_assigned_place_and_wrong_assigned_places) and len(vigilantes_with_assigned_place_and_wrong_assigned_places) > 1:
            vigilant = vigilantes_with_assigned_place_and_wrong_assigned_places[index]
            if len(vigilant.sites_to_look_out) == 1 or vigilant.closet_place not in vigilant.sites_to_look_out:
                index+=1
                continue
            total_assigment_shifts = len(vigilant.shifts)
            assigment_amount_on_closets_place = vigilant.sites_to_look_out.get(vigilant.closet_place)
            #Caso en que la mayoaria de los turnos esta asignado a un solo sitio
            if assigment_amount_on_closets_place / total_assigment_shifts > 0.8:
                if self.change_vigilant_with_most_shifts_in_close_place(solution,vigilant,vigilantes_with_one_wrong_assigned_place):
                    vigilantes_with_one_wrong_assigned_place = self.get_vigilantes_with_one_wrong_assigned_place(solution.vigilantes_schedule)
                    if STOP_GRASP_TWEAK:
                        return solution
                index+=1
            elif assigment_amount_on_closets_place/total_assigment_shifts < 0.2:
                #Cambiar los shifts con un vigilante que se encuentre en un solo sitio y sea el el sitio requerido o mas cercano

                #Cambiar los shifts con un vigilante que contenga su sitio requerido o sitios mas cercano
                if self.change_shifts_from_incorrect_place(vigilant, solution):
                    vigilantes_with_one_wrong_assigned_place = self.get_vigilantes_with_one_wrong_assigned_place(solution.vigilantes_schedule)
                    if STOP_GRASP_TWEAK:
                        return solution
                #Cambiar con vigilantes con sitios mas cercanos
                index+=1
            else:
                #Cambiarlo con un vigilante que tenga solo su sitio rquerido
                #Cambiar los shifts de los que no son el requerido con otros mas cercanos
                if self.change_shifts_from_incorrect_place(vigilant, solution):
                    vigilantes_with_one_wrong_assigned_place = self.get_vigilantes_with_one_wrong_assigned_place(solution.vigilantes_schedule)
                    if STOP_GRASP_TWEAK:
                        return solution
                index+=1


       
        #Cambiar un shift donde este trabajando en otro sitio a su mas cercano
        #Cambiar algunos shifts
        return solution

    def change_vigilant_with_most_shifts_in_close_place(self,solution,vigilant, vigilantes_with_one_wrong_assigned_place) -> bool:
        #Cambiarlo con un vigilante que tenga solo su sitio requerido
        if self.change_vigilant_with_multiple_places_with_vigilant_with_one_place(solution, vigilant , vigilantes_with_one_wrong_assigned_place):
            return True
        #Cambiar Solo los shifts
        if self.change_shifts_from_incorrect_place(vigilant, solution):
            return True
        return False

    def change_place_vigilantes_assigned_to_one_place(self,solution: Solution, vigilantes_with_one_wrong_assigned_place: List[Vigilant]) -> NONE:
        random.shuffle(vigilantes_with_one_wrong_assigned_place)
        index = 0
        while index+1 < len(vigilantes_with_one_wrong_assigned_place):
            vigilant = vigilantes_with_one_wrong_assigned_place[index]
            assigned_site = list(vigilant.sites_to_look_out.keys())[0]
            vigilant_to_change = vigilant
            closest_place_to_assign = assigned_site
            index_change_vigilant = index
            for index_wrong_vigilant in range(len(vigilantes_with_one_wrong_assigned_place)):
                assigned_site_to_change = list(vigilantes_with_one_wrong_assigned_place[index_wrong_vigilant].sites_to_look_out.keys())[0]
                if vigilant_to_change.distances[assigned_site_to_change-1] < vigilant_to_change.distances[closest_place_to_assign-1]:
                    vigilant_to_change = vigilantes_with_one_wrong_assigned_place[index_wrong_vigilant]
                    closest_place_to_assign = assigned_site_to_change
                    index_change_vigilant = index_wrong_vigilant
            #Hacer  el cambio
            if vigilant_to_change != vigilant:
                self.change_assinged_vigilantes_on_site(solution.sites_schedule[assigned_site-1],vigilant,solution.sites_schedule[closest_place_to_assign-1],vigilant_to_change)
                self.change_vigilantes_schedule(vigilant, vigilant_to_change)
                vigilantes_with_one_wrong_assigned_place.remove(vigilant)
                if list(vigilant_to_change.sites_to_look_out.keys())[0] == vigilant_to_change.default_place_to_look_out:
                    vigilantes_with_one_wrong_assigned_place.remove(vigilant_to_change)
                    if index_change_vigilant < index:
                        index-=1
                return True
            else:
                index+=1
        return False
    def change_vigilant_with_multiple_places_with_vigilant_with_one_place(self, solution:Solution, vigilant: Vigilant, vigilantes_with_one_wrong_assigned_place: List[Vigilant]) -> bool:
        for index_wrong_vigilant in range(len(vigilantes_with_one_wrong_assigned_place)):
            vigilant_to_change = vigilantes_with_one_wrong_assigned_place[index_wrong_vigilant]
            assigned_site_to_change = list(vigilant_to_change.sites_to_look_out.keys())[0]
            if assigned_site_to_change == vigilant.closet_place:
                assigned_place_from_vigilant_to_change = solution.sites_schedule[assigned_site_to_change-1]
                assigned_place_from_vigilant_to_change.assigned_Vigilantes.pop(vigilant_to_change.id)
                for site_to_look_out in vigilant.sites_to_look_out:
                    solution.sites_schedule[site_to_look_out-1].assigned_Vigilantes[vigilant_to_change.id] = vigilant_to_change
                    solution.sites_schedule[site_to_look_out-1].assigned_Vigilantes.pop(vigilant.id)             
                solution.sites_schedule[assigned_site_to_change-1].assigned_Vigilantes[vigilant.id] = vigilant
                self.change_vigilantes_schedule(vigilant,vigilant_to_change)
                return True
        return False

    def change_shifts_from_incorrect_place(self, vigilant: Vigilant, solution: Solution):
        change_vigilant = False
        for shift in vigilant.shifts:
            var = False
            site_shift = shift.site_id
            if site_shift != vigilant.closet_place:
                for site_by_distance in vigilant.get_index_sites_by_distance():
                    if site_shift == site_by_distance+1 or vigilant.distances[site_shift -1] < vigilant.distances[site_by_distance] :
                        break
                    for shift_schedule in solution.sites_schedule[site_by_distance].site_schedule:
                        if shift.shift.shift_start == shift_schedule.shift_start and shift.shift.shift_end == shift_schedule.shift_end:
                            for vigilant_on_shift in shift_schedule.assigment_vigilantes:
                                if solution.vigilantes_schedule[vigilant_on_shift-1].closet_place != site_by_distance+1:
                                    shift_to_change = solution.vigilantes_schedule[vigilant_on_shift-1].find_shift_place(shift_schedule)
                                    self.change_shifts_vigilantes(solution.sites_schedule[shift.site_id-1], solution.sites_schedule[site_by_distance], shift, shift_to_change, vigilant, solution.vigilantes_schedule[vigilant_on_shift-1])
                                    var = True
                                    change_vigilant = True
                                    break
                        if var:
                            break
                    if var:
                        break
        return change_vigilant        



    def change_shifts_vigilantes(self, site1: Component, site2: Component, shift1: Shift_place, shift2: Shift_place, vigilant1: Vigilant, vigilant2: Vigilant) -> None:
        self.change_shift_vigilant(site1, site2, shift1, shift2, vigilant1, vigilant2)
        self.change_shift_vigilant(site2, site1, shift2, shift1, vigilant2, vigilant1)

    def change_shift_vigilant(self,actual_site:Component, site_to_change: Component, actual_shift: Shift_place, shift_to_change: Shift_place, actual_vigilant:Vigilant, vigilant_to_change: Vigilant) -> None:
        actual_vigilant.remove_shift(actual_shift)
        actual_vigilant.assign_shift(shift_to_change.shift,shift_to_change.site_id)
        shift_to_change.shift.change_vigilant(vigilant_to_change.id, actual_vigilant.id)
        if actual_site.site_id not in actual_vigilant.sites_to_look_out:
            actual_site.assigned_Vigilantes.pop(actual_vigilant.id)            
        if actual_vigilant.sites_to_look_out.get(site_to_change.site_id) == 1:
            site_to_change.assigned_Vigilantes[actual_vigilant.id] = actual_vigilant

    def change_assinged_vigilantes_on_site(self, actual_site: Component, actual_vigilant:Vigilant, site_to_change:Component, vigilant_to_change: Vigilant) -> None:
        actual_site.assigned_Vigilantes.pop(actual_vigilant.id)
        site_to_change.assigned_Vigilantes.pop(vigilant_to_change.id)
        actual_site.assigned_Vigilantes[vigilant_to_change.id] = vigilant_to_change
        site_to_change.assigned_Vigilantes[actual_vigilant.id] = actual_vigilant

    def change_vigilantes_schedule(self, actual_vigilant:Vigilant, vigilant_to_change: Vigilant) -> None:
        temporal_vigilant = copy.deepcopy(actual_vigilant) 
        self.change_vigilant_schedule(actual_vigilant,vigilant_to_change)
        self.change_vigilant_schedule(vigilant_to_change,temporal_vigilant)

    def change_vigilant_schedule(self, actual_vigilant:Vigilant, vigilant_to_change: Vigilant) -> None:
        actual_vigilant.shifts = vigilant_to_change.shifts
        for shifts_place in actual_vigilant.shifts:
            shifts_place.shift.change_vigilant(vigilant_to_change.id,actual_vigilant.id)
        actual_vigilant.sites_to_look_out = vigilant_to_change.sites_to_look_out
        actual_vigilant.total_hours_worked = vigilant_to_change.total_hours_worked
        actual_vigilant.total_hours_worked_by_week = vigilant_to_change.total_hours_worked_by_week
        actual_vigilant.last_shift = vigilant_to_change.last_shift
    
    def get_vigilantes_with_wrong_assigned_place(self, vigilantes: List[Vigilant]) -> List[List[Vigilant]]:
        vigilantes_with_wrong_assigned_place = [[],[],[]]
        for vigilant in vigilantes:
            if vigilant.closet_place not in vigilant.sites_to_look_out:
                if len(vigilant.sites_to_look_out) == 1:
                    vigilantes_with_wrong_assigned_place[0].append(vigilant)
                else: 
                    vigilantes_with_wrong_assigned_place[2].append(vigilant)
            elif len(vigilant.sites_to_look_out) > 1 :
                vigilantes_with_wrong_assigned_place[1].append(vigilant)
        return vigilantes_with_wrong_assigned_place
    
    def get_vigilantes_with_one_wrong_assigned_place(self, vigilantes: List[Vigilant]) -> List[Vigilant]:
        vigilantes_with_wrong_assigned_place = []
        for vigilant in vigilantes:
            if vigilant.closet_place not in vigilant.sites_to_look_out:
                if len(vigilant.sites_to_look_out) == 1:
                    vigilantes_with_wrong_assigned_place.append(vigilant)
       
        return vigilantes_with_wrong_assigned_place
