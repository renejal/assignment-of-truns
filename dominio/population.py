from os import rename
from pydoc import render_doc
import random
import copy
from re import I
from typing import List, Dict
from urllib import response
from xmlrpc.client import boolean
from isodate import D_DEFAULT
from dominio.Solution import Solution
from dominio.soluction_nsga_ii import SoluctionNsgaII
from dominio.vigilant_assigment import VigilantAssigment
from services.tweak_service import Tweak_service
from conf import settings


class Population():

    __finnest: int
    __soluction_list: List[SoluctionNsgaII]
    __decendets_list: List[SoluctionNsgaII]
    __populations: List[Solution]
    __num_soluction: int 
    __frente: int

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

    def get_solution(self,id: int):
        return self.__populations[id]

    def get_Solutions_of_range(self, id):
        frents: List[Solution]  = []
        for solution in self.__populations:
            if solution.range == id:
                frents.append(solution)
        if frents:
            return frents
        else:
            raise(f"Error: frente con range {id} esta vacio")
            
    def get_soluction_the_frente_whit_range(self, range: int):
        for solution in self.__populations:
            if solution.range_soluction == 1:
                return solution

    def order_by(self, R: List[SoluctionNsgaII]):
        """se ordenas las soluciones dependiendo del rango
        o basado en el numero del frente"""
        """Aquie es donde dentra el ordenamiento no dominda o shorting 
        TODO: ENTENDER EL ALGORITMO DE SHORTING PARA IMPELENTAR ESA FUNCION"""
        pass

    @property
    def populations(self):
        return self.__populations
    @property
    def frente(self):
        return self.__frente
   
    def evaluate_solucion(self, soluction: SoluctionNsgaII):
        """
        la funcion debe guarda en cada atributo de la solucion le valor fitness
        hay que tener en cuenta la funcion de clounding

        :param solucion: la solucion a la que se debe calcular el fitness
        :return: null
        """
        """se encarga de evaluar cad solucion que llegue"""
        pass