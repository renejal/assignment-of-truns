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

    # set
    def mutation_component(self, new_gen: Component, gen_change: Component):
        "se resiven los objetos compoenete luego uno de ellos es de otra solucion y no se puede recupear de esta solucion"
        "TODO: metodo antes que se encarge de validadr las restricciones"
        # en pocas palabar los vigilanes debe intercambia en la misma solucion, pero teneidno en cuenta el orden del componente padre
        if (gen_change or new_gen) != None:
            if gen_change.site_id == new_gen.site_id:
                "si los id son iguales se deberia poder intercambir solo sus vigilantes"
                #intercambiar los vigilanes del componente
            else:
                #1. recuperamos el gen con el cual de va intercambiar el nuevo compotente de la otra solucion padre
                recup_gen_change = copy.copy(gen_change)
                # 1. recuperamos la conincidencia de el sitio y lo eliminamos de la solucion, o busqueda invertida para evitar la eliminacion del gen
                gen_duplicate = self.remove_gen(new_gen.site_id)
                #3. reemplazamos el nuevo gen en la solucion 
                self.add_gen(new_gen)
                #4. reemplazamos el gen 5B old en la coincidencia del nuevo gen de la solucion
                "todo tener en cuentra que los vigilantes pueden etar en varios sitos"
                self.replase(recup_gen_change, get_duplicate)
                #5 agegarmos el gen 5B a la solucion.
                
                self.remove_gen(gen_change.site_id)
        else:
            raise ValueError("los componentes estan vacios")

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


    
