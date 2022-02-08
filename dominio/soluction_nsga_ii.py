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

    def get_random_gen(self, ids_gen_not_avaliable: List[int]):
        response = True
        while response:
            gen =self.sites_schedule[random.randint(0,len(self.sites_schedule))]
            if gen.site_id in ids_gen_not_avaliable:
                print("el componente ya esta la lista")
                continue
            return gen.site_id
        

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

    # set
    def mutation_component(self, id_new_gen: Component, id_gen_change: Component):
        """[mehtod mutation soluciton whit a new gen]

        Args:
            id_gen_add (Component): [new gen in the soluction]
            id_gen_change (Component): [gen the change for id_gen_add]

        Raises:
            ValueError: [empty]
        """
        if (id_gen_change or id_new_gen) != None:
            self.remove_gen(id_gen_change)
            self.add_gen(id_new_gen)
        else:
            raise ValueError("los componentes estan vacios")

    def reparate_component(self, gen_new: Component, gen_change: Component):
        #1. obtener los vigilantes de los dos genes e dientificar que vigilantes son los que se van a intercambiar
        vigilants: List[Vigilant] = gen_new.get_vigilants()



        
        # teniendo en cuenta que un vigilante puede trabajar en varios sitios, se procedek

        pass

    def remove_gen(self, id_gen):
        gen = self.get_gen(id_gen)
        self.sites_schedule.remove(gen)
    
    def add_gen(self, id_gen):
        gen = self.get_gen(id_gen)
        self.sites_schedule.append(gen)
    

    @dominate.setter
    def dominate(self, soluction_id):
       if soluction_id not in self.__dominate:
           self.__dominate.append(soluction_id)
    
    @dominate.setter
    def dominate_me(self, dominate_me_account):
        return self.__dominate_me_account


    
