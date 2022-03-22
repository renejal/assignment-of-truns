import random
import copy
from tkinter.messagebox import NO
from typing import List
from dominio.Solution import Solution
from dominio.model.vigilant import Vigilant
from dominio.Component import Component

class SoluctionNsgaII(Solution):

    __dominate: List[int] 
    __dominate_me_account: int 
    __objetives: int

    def get_random_gen(self, ids_gen_not_avaliable: List[int]) -> Component:
        response = True
        while response:
            gen =self.sites_schedule[random.randint(0,len(self.sites_schedule)-1)]
            if gen.site_id in ids_gen_not_avaliable:
                #"el componente ya esta la lista"
                continue
            return gen
        

    def get_gen(self, gen_id: int) -> Component:
        # note : gen_id = site_id 
        response: Component = None
        for gen in self.sites_schedule:
           if gen.site_id == gen_id:
              response = gen 
              break
        if response:
            return response
        raise ValueError("not found gen whit:",gen_id)
            
    def modification_status(self, value: bool):
        for gen in self.sites_schedule:
            if gen.modified:
                gen.modified = value 
               
        self.sites_schedule
    # get 
    @property
    def dominate(self, position):
        return self.__dominate
    
    @property
    def dominate_me(self):
        return self.__dominate_me

    def crossing_vigilant(self, id_vigilant_new:int, id_vigilant_exchange: int):
        for gen in self.sites_schedule:
            for vigilant_id in gen.assigned_Vigilantes:
                if vigilant_id== id_vigilant_exchange:
                    gen.assigned_Vigilantes.get(vigilant_id).set_id(id_vigilant_new) 
                elif vigilant_id== id_vigilant_new:
                    gen.assigned_Vigilantes.get(vigilant_id).set_id(id_vigilant_exchange)
            
                    
    # set
    def reparate_soluction(self, id_vigilant_new: int, id_vigilant_exchange):
        #recalcualr el fines de la solucion
        pass
 

    def reparate_component(self, gen_new: Component, gen_change: Component):
        vigilants_new: List[Vigilant] = gen_new.get_vigilantes()
        vigilants_change: List[Vigilant] = gen_change.get_vigilantes()

    def remove_gen(self, id_gen):
        "return elimined component"
        gen = self.get_gen(id_gen)
        return self.sites_schedule.pop(gen)
    
    def add_gen(self, gen):
        self.sites_schedule.append(gen)
    
    @dominate.setter
    def dominate_me(self, dominate_me_account):
        return self.__dominate_me_account


    
