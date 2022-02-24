import random
import copy
from typing import List
from dominio.Solution import Solution
from dominio.model.vigilant import Vigilant
from dominio.Component import Component

class SoluctionNsgaII(Solution):

    __dominate: List[int] 
    __dominate_me_account: int 
    __range_soluction: int
    __objetives: int

    # def is_dominate(self, soluction: SoluctionNsgaII):
    #     # se obitene el finter y se compara si domina o no la solucioon
    #     if super().calculate_fitness < soluction.
    #     pass

    def get_random_gen(self, ids_gen_not_avaliable: List[int]) -> Component:
        response = True
        while response:
            gen =self.sites_schedule[random.randint(0,len(self.sites_schedule)-1)]
            if gen.site_id in ids_gen_not_avaliable:
                print("el componente ya esta la lista")
                continue
            return gen
        

    def get_gen(self, gen_id: int):
        # note : gen_id = site_id 
        response: Component
        for gen in self.sites_schedule:
           if gen.site_id == gen_id:
              response = gen 
              break
        if response:
            return response
        raise ValueError("not found gen whit:",gen_id)
            
               
        self.sites_schedule
    # get 
    @property
    def dominate(self, position):
        return self.__dominate
    
    @property
    def dominate_me(self):
        return self.__dominate_me

    @property
    def range_soluction(self):
        return self.__range_soluction

    
    def crossing_vigilant(self, id_vigilant_new:int, id_vigilant_exchange: int):
        for gen in self.sites_schedule:
            for vigilant in gen.assigned_Vigilantes:
                if vigilant.id == id_vigilant_exchange:
                    vigilant.set_id(id_vigilant_new) 
                    gen.modified = True
                    
    # set
    def reparate_soluction(self, id_vigilant_new: int, id_vigilant_exchange):
        for gen in self.sites_schedule:
            for vigilant in gen.assigned_Vigilantes:
                if vigilant.id == id_vigilant_new and not gen.modified:
                    vigilant.set_id(id_vigilant_exchange) 
                    gen.modified = False
                    break
 

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
    def dominate(self, soluction_id):
       if soluction_id not in self.__dominate:
           self.__dominate.append(soluction_id)
    
    @dominate.setter
    def dominate_me(self, dominate_me_account):
        return self.__dominate_me_account


    
