import random
import copy
from typing import List, Dict
from dominio.soluction_nsga_ii import SoluctionNsgaII
from dominio.vigilant_assigment import VigilantAssigment
from services.tweak_service import Tweak_service
from conf import settings

class Population:

    __soluction_list: List[SoluctionNsgaII]
    __decendets_list: List[SoluctionNsgaII]
    __population: List[SoluctionNsgaII]
    __frentes: list[SoluctionNsgaII]

    def not_dominate_sort(self, population: List[SoluctionNsgaII]):
        frentes: List[SoluctionNsgaII] = []
        dominance_list: List[SoluctionNsgaII] = []
        no_dominance_list: List[SoluctionNsgaII] = []
        """ese metodo es el encarda de hacer la ordenameinto no dominad haciendo uso del concepto frente de pareto y reglas de dominancia"""
        for i in range(len(population)):
            population[i].dominate = [] # nueva lista vacia
            population[i].__dominate_me_account= 0 # numero de solucion que la dominan
            population[i].range = -1
            for j in range(len(population)):
                if i == j: continue
                if population[i].is_dominate(population[j]):
                    population[i].add_dominate(population[j])
                else:
                    if population[j].is_dominate(population[i]):
                        population[i].dominate_me += 1 #se incrementar le numero de soluciones que me dominar o domina a esta solucion
            if population[i].dominate_me == 0:
                population[i].range = 1
                # todo: enterner bie nel algoritmo saber en la linea 19 del libre el frente esta siendo asignado a la posion 1 del vector o
                # como es que lo hace. homework
                


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

    def to_dominate(self, soluction_one, soluction_two):
        """LA REGLA DE DOMINANCIA FUNCIOA COMO LA SOLUCION QUE MENORS TENGA VALOR DOMINA A LA OTRAST Y DADO
        EL CASO UNO LLEGAR SER MAYOR NO SERIA DOMINADA"""
        """se define is la solucion es dominada"""
        
        pass

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
