import random
import copy
from typing import List, Dict

from isodate import D_DEFAULT
from dominio.soluction_nsga_ii import SoluctionNsgaII
from dominio.vigilant_assigment import VigilantAssigment
from services.tweak_service import Tweak_service
from conf import settings

class Population:

    __soluction_list: List[SoluctionNsgaII]
    __decendets_list: List[SoluctionNsgaII]
    __population: List[SoluctionNsgaII]
    __frentes: Dict[int,List[SoluctionNsgaII]]

    def not_dominate_sort(self, population: List[SoluctionNsgaII]):
        self.calculate_soluction_dominated(population)
        self.calculate_soluction_for_frentes(population)
                 
    def calculate_soluction_for_frentes(self,soluction):
        range = 1
        while self.get_soluction_the_frente_whit_range(range):
            soluctions_of_range: List[SoluctionNsgaII] = self.get_soluction_the_frente_whit_range(range)
            for soluction_dominate in soluctions_of_range:
                for soluction in soluction_dominate.dominate: 
                    soluction.dominate_me -=1
                    if soluction.dominate_me == 0:
                        soluction.range += 1
                        self.add_frente(soluction, range + 1)
            range += 1
       
    def calculate_soluction_dominated(self, population: List[SoluctionNsgaII]):
         for i in range(len(population)):
            population[i].dominate = [] # nueva lista vacia
            population[i].__dominate_me_account= 0 # numero de solucion que la dominan
            population[i].range = -1
            for j in range(len(population)):
                if i == j: continue
                if self.to_dominate(population[i],population[j]):
                    population[i].add_dominate(population[j].id)
                else:
                    if self.to_dominate(population[j],population[i]):
                        population[i].dominate_me += 1 #se incrementar le numero de soluciones que me dominar o domina a esta solucion
            if population[i].dominate_me == 0:
                population[i].range = 1
                self.add_frente(population[i],1)

    def add_dominate(self, soluction_dominate: SoluctionNsgaII, soluction_dominate_me: SoluctionNsgaII):
        "add tha dominate soluction a tha list of soluction that dominates it"
    
    def add_frente(self, soluction: SoluctionNsgaII, range: int):
        dominate = self.__frentes.get(range) 
        if not dominate:
            self.__frentes[range] = [soluction]
        else:
            if soluction not in dominate:
                dominate.append(soluction)

    def get_soluction_the_frente_whit_range(self, range: int) -> SoluctionNsgaII:
        return self.__frentes.get(range)
        
        
    def inicialize_population(self, problem: VigilantAssigment, soluction_number: int) -> List[SoluctionNsgaII]:
        """la idea seria llmaar los metodo s de GRAS que tuilizan para genear los componentes y asi
        logra genear una soluion e ir armando la poblacion inicial, creo  que es la mejor opcion"""
        for k in range(soluction_number):
            S = SoluctionNsgaII(problem, settings)
            while S.is_solution_complete():
                components = S.create_components(soluction_number)
                component = components[random.randint(0, len(components))]
                S.merge_component(component)
            # self.population.append(S)

    def generate_decendents(self, parents: List[SoluctionNsgaII], num_decendets_for_dad: int) -> List[SoluctionNsgaII]:
        """
        se obtiene a partir de una metodo de mutacion, de cruce y de selección
        genera un numero determinado de desendientes a partir de un conjunto de soluciónes del self.soluction_list
        :param soluction:
        :return:
        """
        list_children: list[SoluctionNsgaII] = []
        for iteration in range(num_decendets_for_dad):
            children: SoluctionNsgaII
            for parent in parents:
                "TODO: los hijos generados debe ser mejores que sus padres??"
                children = Tweak_service().Tweak(copy.copy(parent))
                list_children.append(children)
        return list_children

    def to_dominate(self, soluction_one: SoluctionNsgaII, soluction_two: SoluctionNsgaII):
        "compare if tha soluction one dominate a the soluction two"
        response = False
        if soluction_one.calculate_fitness() < soluction_two.calculate_fitness:
            response = True 
        return response

    def order_by(self, R: List[SoluctionNsgaII]):
        """se ordenas las soluciones dependiendo del rango
        o basado en el numero del frente"""
        """Aquie es donde dentra el ordenamiento no dominda o shorting 
        TODO: ENTENDER EL ALGORITMO DE SHORTING PARA IMPELENTAR ESA FUNCION"""
        pass

    def union_soluction(self, parents, children) -> List[SoluctionNsgaII]:
        """se encarda de unir los padres y los hijos de una misma lista y luego la ordena porn RANGO"""
        "return una lista unida de padres he hijos"
        return  parents + children



    def get_front_the_pareto(self):
        """el frende de pareto es se puede dividir en rangos
        rango 1 : para el conjunto de solucion del frente de pareto
        rango 2 : para el conjunt ode soluciones que estan mas serca al confunto de rango 1 del frente de pareto
        """
        pass


    def evaluate_solucion(self, soluction: SoluctionNsgaII):
        """
        la funcion debe guarda en cada atributo de la solucion le valor fitness
        hay que tener en cuenta la funcion de clounding

        :param solucion: la solucion a la que se debe calcular el fitness
        :return: null
        """
        """se encarga de evaluar cad solucion que llegue"""
        pass