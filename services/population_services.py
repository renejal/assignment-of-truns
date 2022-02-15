import imp
import copy
import random
from re import I
from urllib import response
from conf import settings 
from typing import List, Dict
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
            childrens.append(PopulationServices.parent_crossing(parent_for_exchange_one, parent_for_exchange_two))  
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

    def validation_size():
        pass 

    @staticmethod
    def is_validation_and_repartion(list_vigilants_one: List[Vigilant], list_vigilants_two: List[Vigilant]):
        "validat and reparation of list for what are compatible"
        validation_response = False
        while True:
            if (len(list_vigilants_one) == len(list_vigilants_two)) and (len(list_vigilants_two) and len(list_vigilants_one)) >0:
                validation_response =  True
                break
            elif (len(list_vigilants_one) > len(list_vigilants_two)) and len(list_vigilants_one)>0:
                list_vigilants_one.remove(random.randint(0,len(list_vigilants_one)-1))
            elif (len(list_vigilants_one) < len(list_vigilants_two)) and len(list_vigilants_two) > 0:
                list_vigilants_two.remove(random.randint(0,len(list_vigilants_two)-1))
            else:
                break
        return validation_response
             
    @staticmethod
    def get_random_gen_with_their_vigilant(parent_for_exchange_one: SoluctionNsgaII, parent_for_exchange_two: SoluctionNsgaII) -> Dict:
        iteration = 0
        while iteration <= settings.NUMBER_ITERATION_SELECTION_COMPONENTE:
            gen_parent_for_exchange_one: Component = parent_for_exchange_one.get_random_gen([])
            vigilants_new: List[Vigilant] = [vigilant for vigilant in gen_parent_for_exchange_one.assigned_Vigilantes if vigilant.fault_place_to_look_out != -1]
            gen_parent_exchange_two: Component = parent_for_exchange_two.get_random_gen([gen_parent_for_exchange_one])
            vigilants_exchange: List[Vigilant] = [vigilant for vigilant in gen_parent_exchange_two.assigned_Vigilantes if vigilant.default_place_to_look_out != -1]
            if PopulationServices.is_validation_and_repartion(vigilants_new, vigilants_exchange):
                return vigilants_new , vigilants_exchange
            iteration += 1
        raise("error: NO found gens that accomplished constraint for site")


    @staticmethod
    def parent_crossing(parent_for_exchange_one: SoluctionNsgaII, parent_for_exchange_two: SoluctionNsgaII) -> SoluctionNsgaII:
        """_crossing of thow soluction parent, vigilantnew is the vigilants that arrive and they will be exchange for vigilants_exchange"""
        # vigilant_new : list : vigilants of a site of tha soluction one
        # vigilant_exchange: list: vigilants of a site of tha soluction two 
        for vigilant_id_one, vigilant_id_two in zip(vigilants_new, vigilants_exchange):
                PopulationServices.exchange_vigilant_between_soluction(
                    gen_parent_for_exchange_one, vigilant_id_one,
                    gen_parent_exchange_two, vigilant_id_two)

        # Tweak_assignment_vigilantes_amount().exchange_shift(parent_for_exchange_one.shi, vigilants_new[i], vigilants_exchange[i])
        # invercambiar vigilants(vigilant_di, vigilant_id)

        return parent_for_exchange_one, parent_for_exchange_two

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

