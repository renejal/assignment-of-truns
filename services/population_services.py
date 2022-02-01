import copy
from typing import List, Dict
from dominio.soluction_nsga_ii import SoluctionNsgaII
from services.tweak_service import Tweak_service
class PopulationServices:

    @staticmethod
    def generate_decendents(parents: List[SoluctionNsgaII], num_decendets_for_fatherd: int) -> List[SoluctionNsgaII]:
        list_children: list[SoluctionNsgaII] = []
        for iteration in range(num_decendets_for_fatherd):
            children: SoluctionNsgaII
            for parent in parents:
                "TODO: los hijos generados debe ser mejores que sus padres??"
                children = Tweak_service().Tweak(copy.copy(parent))
                list_children.append(children)
        return list_children

    @staticmethod
    def union_soluction(parents, children) -> List[SoluctionNsgaII]:
        """se encarda de unir los padres y los hijos de una misma lista y luego la ordena porn RANGO"""
        "return una lista unida de padres he hijos"
        return  parents + children

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

