import copy
from typing import List, Dict

from numpy import var
from dominio.Solution import Solution
# from dominio.soluction_nsga_ii import Solution
from dominio.vigilant_assigment import VigilantAssigment
from services.tweak_service import Tweak_service
from conf import settings
import pprint

class Population():

    __finnest: int
    __soluction_list: List[Solution]
    __decendets_list: List[Solution]
    __populations: List[Solution]
    __num_soluction: int
    __frente: Dict[int,List[Solution]] # el indice del la lista representa el rango del frente 0: rango 0 del frente de pareto

    def __init__(self, problem: VigilantAssigment = None, num_soluction: int = None, population = None):
        self.__num_soluction = settings.SIZE_POPULATION
        self.__populations = population
        self.problem = problem
        self.__frente = {} 

    def is_soluction_complete(self):
        response = False 
        if len(self.populations) > self.__num_soluction:
           response = True 
        return response

    def add_dominate(self, soluction_dominate: Solution, soluction_dominate_me: Solution):

        "add tha domiNAte soluction a tha list oF soluction that dominates it"
        pass 
    

    def inicialize_population(self) -> List[Solution]:
        """la idea seria llmaar los metodo s de GRAS que tuilizan para genear los componentes y asi
        logra genear una soluion e ir armando la poblacion inicial, creo  que es la mejor opcion"""
        population: List[Solution] = []
        for i in range(self.__num_soluction):
            S = Solution(self.problem)
            while S.is_solution_complete():
                components = S.create_components(self.__num_soluction)
                restried_list = components 
                if restried_list == None:
                    continue
                else:
                    best_restricted_list = S.get_best_components(restried_list, settings.RESTRICTED_LIST_AMOUNT_COMPONENT)
                    S.merge_component(best_restricted_list)            
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
        if frents:
            return frents
        else:
            return False
    
    def get_populations(self, num_soluction):
        population = []
        rango = 1
        while len(population) < num_soluction:
            population = population + self.get_Solutions_of_range(rango)
            rango = +1
        if len(population) <= num_soluction:
            raise("No se encontro el numero de soluciones requeridas")
        return population[:num_soluction]

    def get_soluction_the_frente_whit_range(self, range: int):
        for solution in self.__populations:
            if solution.range_soluction == 1:
                return solution

    def order_by(self, R: List[Solution]):
        """se ordenas las soluciones dependiendo del rango
        o basado en el numero del frente"""
        """Aquie es donde dentra el ordenamiento no dominda o shorting 
        TODO: ENTENDER EL ALGORITMO DE SHORTING PARA IMPELENTAR ESA FUNCION"""
        pass

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
     
    def evaluate_solucion(self, soluction: Solution):
        """
        la funcion debe guarda en cada atributo de la solucion le valor fitness
        hay que tener en cuenta la funcion de clounding

        :param solucion: la solucion a la que se debe calcular el fitness
        :return: null
        """
        """se encarga de evaluar cad solucion que llegue"""
        pass