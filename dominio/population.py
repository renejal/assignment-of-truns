from os import rename
from pydoc import render_doc
import random
import copy
from re import I
from typing import List, Dict
from urllib import response
from xmlrpc.client import boolean
from isodate import D_DEFAULT
from dominio.soluction_nsga_ii import SoluctionNsgaII
from dominio.vigilant_assigment import VigilantAssigment
from services.tweak_service import Tweak_service
from conf import settings


class Population():

    __finnest: int
    __soluction_list: List[SoluctionNsgaII]
    __decendets_list: List[SoluctionNsgaII]
    __populations: List[SoluctionNsgaII]
    __num_soluction: int 

    def __init__(self, problem: VigilantAssigment, num_soluction: int):
        self.__num_soluction = num_soluction
        self.__populations= self.inicialize_population(problem, num_soluction)
    

    def is_soluction_complete(self):
        response = False 
        if len(Population) < self.__num_soluction:
           response = True 
        return response

    def add_dominate(self, soluction_dominate: SoluctionNsgaII, soluction_dominate_me: SoluctionNsgaII):

        "add tha domiNAte soluction a tha list oF soluction that dominates it"
        pass 
    
    @staticmethod
    def add_frente(soluction: SoluctionNsgaII, soluction_range: int, frente: Dict[int,List[SoluctionNsgaII]]):
        dominate = frente.get(soluction_range) 
        if not dominate:
            frente[soluction_range] = [soluction]
        else:
            if soluction not in dominate:
                dominate.append(soluction)

    @staticmethod
    def get_soluction_the_frente_whit_range(range: int) -> SoluctionNsgaII:
        return frente.get(range)
        
        
    def inicialize_population(self, problem: VigilantAssigment, soluction_number: int) -> List[SoluctionNsgaII]:
        """la idea seria llmaar los metodo s de GRAS que tuilizan para genear los componentes y asi
        logra genear una soluion e ir armando la poblacion inicial, creo  que es la mejor opcion"""
        population: List[SoluctionNsgaII] = []
        for i in range(soluction_number):
            S = SoluctionNsgaII(problem, settings)
            while S.is_solution_complete():
                components = S.create_components(soluction_number)
                restried_list = components 
                if restried_list == None:
                    continue
                else:
                    best_restricted_list = S.get_best_components(restried_list, settings.RESTRICTED_LIST_AMOUNT_COMPONENT)
                    S.merge_component(best_restricted_list)            
            population.append(S) 
        return population 

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

    @staticmethod
    def to_dominate(soluction_one: SoluctionNsgaII, soluction_two: SoluctionNsgaII)-> bool:
        #TODO: test for method
        response = False
        number_of_objetives = len(soluction_one.objectives_to_optimize)
        for j in range(number_of_objetives):
            if soluction_one.objectives_to_optimize[j] < soluction_two.objectives_to_optimize[j]:
                response = True
            else:
                if soluction_one.objectives_to_optimize[j] < soluction_two.objectives_to_optimize[j]:
                    return False
        return response

    def order_by(self, R: List[SoluctionNsgaII]):
        """se ordenas las soluciones dependiendo del rango
        o basado en el numero del frente"""
        """Aquie es donde dentra el ordenamiento no dominda o shorting 
        TODO: ENTENDER EL ALGORITMO DE SHORTING PARA IMPELENTAR ESA FUNCION"""
        pass

    @property
    def populations(self):
        return self.__populations
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