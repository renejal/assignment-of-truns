import imp
import copy
import random
from re import I
from urllib import response
from conf import settings 
from typing import List, Dict, Tuple
from dominio.model.vigilant import Vigilant
# from msilib.schema import Component
from dominio.soluction_nsga_ii import SoluctionNsgaII
from dominio.Component import Component
from services.tweak_assignment_vigilantes_amount import Tweak_assignment_vigilantes_amount

class PopulationServices:

    @staticmethod
    def generate_decendents(population: List[SoluctionNsgaII], number_of_children: int) -> List[SoluctionNsgaII]:
        "a copy of tha populaton is received"
        childrens: list[SoluctionNsgaII] = []
        while len(population)>1:
            parents = PopulationServices.get_parents(population)
            childrens.append(PopulationServices.mating_between_parents(parents[0],parents[1], number_of_children))
        return childrens
    
    @staticmethod
    def get_parents(parents: List[SoluctionNsgaII]) -> List[SoluctionNsgaII]:
        response: List[SoluctionNsgaII] = []
        response.append(parents.pop(random.randint(0, len(parents)-1)))
        response.append(parents.pop(random.randint(0, len(parents)-1)))
        return response

    @staticmethod
    def mating_between_parents(parent_for_exchange_one: SoluctionNsgaII, parent_for_exchange_two: SoluctionNsgaII, number_of_children) -> SoluctionNsgaII:
        "maing between parent_one and parent"
        childrens: List[SoluctionNsgaII] = []
        for i in range(number_of_children):
            childrens.append(PopulationServices.parent_crossing(parent_for_exchange_one,parent_for_exchange_two))  
        return PopulationServices.get_best_children(childrens)
        
    @staticmethod
    def get_best_children(childrens: List[SoluctionNsgaII]) -> SoluctionNsgaII:
        best: SoluctionNsgaII  = None
        for children in childrens:
            if best == None:
                best = children 
                continue
            if children.total_fitness > best.total_fitness:
                best = children
        return best

    def remove_vigilants_default_the_site(gen: Component):
        Vigilants: List[Vigilant] = gen.assigned_Vigilantes
        for vigilant in Vigilants:
            if vigilant.default_place_to_look_out == -1:
                Vigilants.remove(vigilant)
        
    @staticmethod
    def is_validation_and_repartion(gen_new: Component, gen_of_exchange: Component): 
        #return true si el methodos remove..(gen_..) retorna lista de vigilantes no vacias
        status = False
        if PopulationServices.remove_vigilants_default_the_site(gen_new):
            if PopulationServices.remove_vigilants_default_the_site(gen_of_exchange):
                status = True
        return status
             
    @staticmethod
    def get_random_gens(parent_for_exchange_new: SoluctionNsgaII, parent_for_exchange: SoluctionNsgaII) -> List[Component]:
        "El metodo debe retornas la lista de vigilantes del componente y el componente del cual fue sacado"
        gen_parent_for_exchange_new: Component = None
        gen_parent_exchange: Component = None
        iteration = 0
        while iteration <= settings.NUMBER_ITERATION_SELECTION_COMPONENTE:
            gen_parent_for_exchange_new = parent_for_exchange_new.get_random_gen([])
            gen_parent_exchange = parent_for_exchange.get_random_gen([gen_parent_for_exchange_new])
            if PopulationServices.is_validation_and_repartion(gen_parent_for_exchange_new, gen_parent_exchange):
                break
            iteration += 1
        if gen_parent_exchange or gen_parent_for_exchange_new:
            return [gen_parent_exchange, gen_parent_exchange]
        raise("Error, no se encontro genes que cumplan con las requerimientos")

    @staticmethod
    #todo debe resibir una copia de los parametros
    def parent_crossing(parent_for_exchange_new: SoluctionNsgaII, parent_for_exchange: SoluctionNsgaII) -> SoluctionNsgaII:
        genes: List[Component] = PopulationServices.get_random_gens(copy.copy(parent_for_exchange_new),copy.copy(parent_for_exchange))
        for vigilant_new, vigilant_for_exchagen in zip(genes[0].assigned_Vigilantes, genes[1].assigned_Vigilantes):
                #TODO: INTERCAMBIA RVIGILANTES, ya tenemos los vigialntes filtrados y listos, se debe mirar la forma de como intercambair 
                #los vigilantes en el componente espesifico 
                
                PopulationServices.exchange_vigilant_between_soluction(vigilant_new.id, vigilant_for_exchagen.id)
        else:
            raise("error no se encontro vigilantes para cruse")    

    @staticmethod
    def exchange_vigilant_between_soluction(self, gen_parent_for_exchange_one: Component, exchange_vigilant_id_one: Vigilant, 
                                            gen_parent_exchange_two: Component, exchange_vigilant_id_two: Component):
        exchange_vigilant_id_one.set_id(exchange_vigilant_id_two.id)
        exchange_vigilant_id_two.set_id(exchange_vigilant_id_one.id)
 
    @staticmethod
    def mutation_component(gen_for_exchange_one: Component, exchange_gen_before_two: Component):
        if (gen_for_exchange_one and exchange_gen_before_two) != None:
            vigilants_new = [vigilant.id for vigilant in gen_for_exchange_one.assigned_Vigilantes if vigilant.fault_place_to_look_out != -1]
            vigilants_exchange = [vigilant.id for vigilant in exchange_gen_before_two.assigned_Vigilantes if vigilant.default_place_to_look_out != -1]
            if (len(vigilants_new) and len(vigilants_exchange)) > 0:
                for vigilant_id in vigilants_new:
                    # Tweak_assignment_vigilantes_amount().exchange_shift(shif_place, vigilants_new[i], vigilants_exchange[i])
                    recup_gen_change = copy.copy(exchange_gen_after)
                    # 1. recuperamos la conincidencia de el sitio y lo eliminamos de la solucion, o busqueda invertida para evitar la eliminacion del gen
                    gen_duplicate = self.remove_gen(new_gen_for_exchange.site_id)
                    #3. reemplazamos elnuevo oen en la solucion 
                    self.add_gen(new_gen_for_exchange)
                    #4. reemplazamos el gen 5B old en la coincidencia del nuevo gen de la solucion
                    "todo tener en cuentra que los vigilantes pueden etar en varios sitos"
                    self.replase(recup_gen_change, get_duplicate)
                    #5 agegarmos el gen 5B a la solucion.
                    
                    self.remove_gen(exchange_gen_after.site_id)
        else:
            raise ValueError("los componentes estan vacios")

    def reparate_component(self, gen_new: Component, gen_change: Component):
        vigilants_new: List[Vigilant] = gen_new.get_vigilantes()
        vigilants_change: List[Vigilant] = gen_change.get_vigilantes()

    @staticmethod
    def union_soluction(parents, children) -> List[SoluctionNsgaII]:
        """se encarda de unir los padres y los hijos de una misma lista y luego la ordena porn RANGO"""
        "return una lista unida de padres he hijos"
        return  parents + children
    
    @staticmethod
    def not_dominate_sort(population: List[SoluctionNsgaII])-> Dict[int,List[SoluctionNsgaII]]:
        population: List[SoluctionNsgaII]
        frentes: Dict[int,List[SoluctionNsgaII]]
        PopulationServices.calculate_soluction_dominated(population, frentes)
        PopulationServices.calculate_soluction_for_frentes(population, frentes)
        return frentes

    def calculate_soluction_for_frentes(self, soluction: SoluctionNsgaII, frentes: Dict[int, List[SoluctionNsgaII]]):
        range_soluction = 1
        while self.get_soluction_the_frente_whit_range(range_soluction):
            soluctions_of_range: List[SoluctionNsgaII] = self.get_soluction_the_frente_whit_range(range_soluction)
            for soluction_dominate in soluctions_of_range:
               for soluction in soluction_dominate.dominate: 
                    soluction.dominate_me -=1
                    if soluction.dominate_me == 0:
                        soluction.range += 1
                        self.add_frente(soluction, range_soluction+ 1)
            range_soluction += 1

        return frentes



    @staticmethod
    def calculate_soluction_dominated(population: List[SoluctionNsgaII], frente: List[SoluctionNsgaII]):

        for i in range(len(population)):
            population[i].dominate = [] # nueva lista vacia
            population[i].__dominate_me_account= 0 # numero de solucion que la dominan
            population[i].range_soluction = -1
            for j in range(len(population)):
                if i == j: continue
                if self.to_dominate(population[i],population[j]):
                    population[i].add_dominate(population[j].id)
                else:
                    if self.to_dominate(population[j],population[i]):
                        population[i].dominate_me += 1 #se incrementar le numero de soluciones que me dominar o domina a esta solucion
            if population[i].dominate_me == 0:
                population[i].range_soluction = 1
                self.add_frente(population[i],1, frente)

