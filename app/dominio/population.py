import copy
import time
from typing import List, Dict

from dominio.Solution import Solution
from dominio.vigilant_assigment import VigilantAssigment
from services.tweak_service import Tweak_service
from conf import settings

class Population():

    __populations: List[Solution]
    __num_soluction: int
    __frente: Dict[int,List[Solution]] # el indice del la lista representa el rango del frente 0: rango 0 del frente de pareto

    def __init__(self, problem: VigilantAssigment = None, num_soluction: int = None, population = None):
        self.__num_soluction = settings.POPULATION_AMOUNT_NSGAII
        self.__populations = population
        self.problem = problem
        self.__frente = {} 

    def is_soluction_complete(self):
        response = False 
        if len(self.populations) > self.__num_soluction:
           response = True 
        return response

    def inicialize_population(self, maxTime) -> List[Solution]:
        """la idea seria llaar los metodo s de GRAS que tuilizan para genear los componentes y asi
        logra genear una soluion e ir armando la poblacion inicial, creo  que es la mejor opcion"""
        print("Getting started population")
        population: List[Solution] = []
        for i in range(self.__num_soluction):
            current_timeout = time.time()
            if(current_timeout > maxTime and len(population >= 2)):
                self.populations = population 
            S = Solution(self.problem)
            while S.is_solution_complete():
                components = S.create_components(1)
                S.merge_component(components[0])            
            population.append(S) 
        self.populations = population 

    def generate_decendents(self, parents: List[Solution], num_decendets_for_dad: int) -> List[Solution]:
        """
        se obtiene a partir de una metodo de mutacion, de cruce y de selección
        genera un numero determinado de desendientes a partir de un conjunto de soluciónes del self.soluction_list
        :param soluction:
        :return:
        """
        list_children: List[Solution] = []
        for iteration in range(num_decendets_for_dad):
            children: Solution
            for parent in parents:
                "TODO: los hijos generados debe ser mejores que sus padres??"
                children = Tweak_service().Tweak(copy.copy(parent))
                list_children.append(children)
        return list_children

    def get_solution(self,id: int):
        return self.__populations[id]

    def get_Solutions_of_range(self, rango):
        frents: List[Solution]  = []
        for solution in self.__populations:
            if solution.range == rango:
                frents.append(solution)
        return frents
    
    def get_populations(self, num_soluction):
        population = []
        rango = 1
        while len(population) < num_soluction:
            population = population + self.get_Solutions_of_range(rango)
            rango = +1
        if len(population) <= num_soluction:
            return population
            # raise("No se encontro el numero de soluciones requeridas")
        return population[:num_soluction]

    def get_soluction_the_frente_whit_range(self, range: int):
        for solution in self.__populations:
            if solution.range_soluction == 1:
                return solution

    @property
    def populations(self):
        return self.__populations

    @populations.setter
    def populations(self, population: List[Solution]):
        self.__populations = population

    @property
    def frente(self):
        return self.__frente
    
    def add_frente(self, key, value):
        solutions = self.__frente.get(key)
        if solutions:
            solutions.append(value)
        else:
            self.__frente[key]=[value]

    @frente.setter
    def frente(self, list_soluction: List[Solution]):
        self.__frente = list_soluction
     