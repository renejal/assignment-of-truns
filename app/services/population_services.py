import copy
import random
from re import I
from conf import settings 
from typing import List, Tuple
from dominio.model.vigilant import Vigilant
from dominio.population import Population
# from msilib.schema import Component
# from dominio.soluction_nsga_ii import Solution
from dominio.Solution import Solution
from dominio.Solution import Solution
from dominio.Component import Component
from services.tweak_assignment_vigilantes_amount import Tweak_assignment_vigilantes_amount

class PopulationServices:

    @staticmethod
    def generate_decendents(population: List[Solution]) -> List[Solution]:
        "a copy of tha populaton is received"
        childrens: list[Solution] = []
        while population: 
            parents = PopulationServices.get_parents(population)
            #TODO: GENEAR DOS HIJOS POR DOS PADRES, 
            children = PopulationServices.mating_between_parents(parents[0],parents[1])
            childrens.append(children[0])
            childrens.append(children[1])
        return childrens
    
    @staticmethod
    def get_parents(parents: List[Solution]) -> List[Solution]:
        response: List[Solution] = []
        response.append(parents.pop(random.randint(0, len(parents)-1)))
        response.append(parents.pop(random.randint(0, len(parents)-1)))
        return response
    
    @staticmethod
    def calculate_fitness(childrens: List[Solution]):
        # calcular fitness para cada solucion de la lista childrens
        for children in childrens:
            children.calculate_fitness()

    @staticmethod
    def mating_between_parents(parent_for_exchange_one: Solution, parent_for_exchange_two: Solution) -> Solution:
        childrens: List[Solution] = []
        for i in range(settings.NUMBER_OF_CHILDREN_GENERATE):
            child = PopulationServices.parent_crossing(copy.copy(parent_for_exchange_one),copy.copy(parent_for_exchange_two))
            if child:
                childrens.append(child)  
            elif childrens:
                #retorna la dos mejores soluciones
                PopulationServices.calculate_fitness(childrens)
                childrens = PopulationServices.get_best_Soluction(childrens, parent_for_exchange_one, parent_for_exchange_two)
        else:
            # si no encuetra soluciones mejores retorna los padres iniciales TODO: MIAR LA FORMA DE MEJORA ESTO, TAL VEZ RESTRINGIENDO ESTAS SOLUCIONES
            childrens.append(parent_for_exchange_one)
            childrens.append(parent_for_exchange_two)
        return childrens

    @staticmethod
    def get_best_Soluction(childrens: List[Solution], parent_for_exchange_one: Solution, parent_for_exchange_two: Solution):
        for i in range(1):
            best = PopulationServices.get_best_children_of_childrens_list(childrens)
            if best.total_fitness < (parent_for_exchange_one.total_fitness or parent_for_exchange_two.total_fitness):
                childrens.append(best)
        if len(childrens) == 1:
            best = parent_for_exchange_one if parent_for_exchange_one.total_fitness < parent_for_exchange_two.total_fitness else parent_for_exchange_two.total_fitness
            childrens.append(best)
        return childrens
        
    @staticmethod
    def get_best_children_of_childrens_list(childrens: List[Solution]) -> Solution:
        best: Solution  = None
        for children in childrens:
            if best == None:
                best = children 
                continue
            if children.total_fitness > best.total_fitness:
                best = children
        childrens.remove(best)
        return best

    def remove_vigilants_default_the_site(gen: Component):
        Vigilants: List[Vigilant] = gen.assigned_Vigilantes
        for vigilant in Vigilants:
            if vigilant.default_place_to_look_out == -1:
                Vigilants.remove(vigilant)
        
    @staticmethod
    def is_validation_and_repartion(gen_new: Component, gen_exchange: Component): 
        vigilants_new: List[int] = [vigilant for vigilant in gen_new.assigned_Vigilantes]
        vigilants_exchange: List[int] = [vigilant for vigilant in gen_exchange.assigned_Vigilantes]

        if (vigilants_new and vigilants_exchange) == []:
            return None

        diference = list(set(vigilants_new) - set(vigilants_exchange))
        diference += list(set(vigilants_exchange) - set(vigilants_new))
        if not diference:
            return None
        vigilants_new_not_in_commont: List[int] = [vigilant for vigilant in gen_new.assigned_Vigilantes if vigilant in diference and gen_new.get_vigilant(vigilant).default_place_to_look_out == -1]
        vigilants_exchange_not_in_commont: List[int] = [vigilant for vigilant in gen_exchange.assigned_Vigilantes if vigilant in diference and gen_exchange.get_vigilant(vigilant).default_place_to_look_out == -1]
        return vigilants_new_not_in_commont, vigilants_exchange_not_in_commont

    @staticmethod
    def get_random_gens(parent_for_exchange_new: Solution, parent_for_exchange: Solution) -> List[Component]:
        "El metodo debe retornas la lista de vigilantes del componente y el componente del cual fue sacado"
        gen_parent_for_exchange_new: Component = None
        gen_parent_exchange: Component = None
        iteration = 0
        while iteration <= settings.NUMBER_ITERATION_SELECTION_COMPONENTE:
            gen_parent_for_exchange_new = parent_for_exchange_new.get_random_gen([])
            gen_parent_exchange = parent_for_exchange.get_random_gen([gen_parent_for_exchange_new.site_id])
            # vigilants_new, vigilants_exchanges = PopulationServices.is_validation_and_repartion(gen_parent_for_exchange_new, gen_parent_exchange)
            result = PopulationServices.is_validation_and_repartion(gen_parent_for_exchange_new, gen_parent_exchange)
            if not result:
                return False
            if (result[0] and result[1]) != [] and (result[0] and result[1]) is not None:
                return result[0], result[1]

            # if (resultvigilants_new and vigilants_exchanges) != [] and (vigilants_new and vigilants_exchanges) is not None:
            #     return [vigilants_new, vigilants_exchanges]
            iteration += 1
        return False
        raise("Error no se encontro vigilantes disponibles")

    @staticmethod
    #todo debe resibir una copia de los parametros
    def parent_crossing(parent_for_exchange_new: Solution, children: Solution) -> Solution:
        "el hijo va hacer  una copia de la nueva solucion con su respectiva mutacion"
        vigilants: List[Component] = PopulationServices.get_random_gens(copy.copy(parent_for_exchange_new),copy.copy(children)) #TODO: los vigilantes deven ser diferentes en las dos listas
        if not vigilants:
            return False
        for vigilant_new_id, vigilant_for_exchagen_id in zip(vigilants[0], vigilants[1]):
                children.crossing_vigilant(vigilant_new_id, vigilant_for_exchagen_id)
                # children.reparate_soluction(vigilant_new_id, vigilant_for_exchagen_id) # TODO: RECALCULAR FIENES Y REFPACION
        return children

    @staticmethod
    def union_soluction(parents, children) -> List[Solution]:
        return  parents + children
    

    @staticmethod
    def to_dominate(soluction_one: Solution, soluction_two: Solution)-> bool:
        #TODO: test for method
        response = False
        number_of_objetives = len(soluction_one.fitness)
        for j in range(number_of_objetives):
            if soluction_one.fitness[j] < soluction_two.fitness[j]:
                response = True
            else:
                if soluction_two.fitness[j] < soluction_one.fitness[j]:
                    return False
        return response

    @staticmethod
    def not_dominate_sort(population: Population) -> List[Solution]:
        PopulationServices.add_ids_solution(population.populations)
        PopulationServices.calculate_dominance(population)
        PopulationServices.calculate_range(population)
        return population.frente

    @staticmethod
    def add_ids_solution(population: List[Solution]):
        try:
            for index, solution in enumerate(population):
                solution.id = index + 1
        except:
            raise("error population",population)

    @staticmethod
    def calculate_range(population: Population):
        rango = 1
        while population.frente.get(rango): # rango 1 del frente de pareto
            solutions: List[Solution] = population.frente.get(rango)
            for dominated_solution in solutions:
               for solution_id in dominated_solution.dominated:
                    solution = PopulationServices.get_solution(population.populations,solution_id)
                    if not solution: break # no ecuentra la solution 5
                    solution.dominate_me -=1
                    if solution.dominate_me == 0:
                        r=rango+1
                        solution.range=r 
                        population.add_frente(key=range,value=solution)
                    print("solution_id")
                    print(solution.id)
                    print(solution.range)
            rango +=1

    @staticmethod
    def get_solution(population: List[Solution], id_solution: int):
        for solution in population:
            if solution.id == id_solution:
                return solution
        return False
    @staticmethod
    def get_frente(population: List[Solution], range):
        frente: List[Solution] = []
        for solution in population:
            if solution.range == range:
                frente.append(solution)
        return frente 

    @staticmethod
    def get_solutions_by_frente(population: List[Solution], amount:int):
        frente: List[Solution] = []
        if len(population) < amount:
            amount = len(population)
        range = 1
        while len(frente) < amount:
            for solution in population:
                if solution.range == range:
                    frente.append(solution)
                    if len(frente) == amount:
                        return frente
            range+=1 
        return frente

    @staticmethod
    def calculate_dominance(population_object: Population):
        population = population_object.populations
        for i in range(len(population)):
            population[i].dominated=[] # nueva lista vacia
            population[i].__dominate_me_account= 0 # numero de solucion que la dominan
            population[i].range= -1
            for j in range(len(population)):
                if i == j: continue
                if PopulationServices.to_dominate(population[i],population[j]): # la solucion i domina a la solucion j ?
                    population[i].add_dominate(population[j].id)
                else:
                    if PopulationServices.to_dominate(population[j],population[i]):
                        population[i].dominate_me += 1 #se incrementar le numero de soluciones que me dominar o domina a esta solucion
            if population[i].dominate_me == 0:
                population[i].range= 1
                population_object.add_frente(key=1,value=population[i])
    
    def distance_crowding(population: Population):
        frente = population.populations
        rango = PopulationServices.get_range_of_objective(frente)
        for solution in frente:
            solution.crowding_distance = 0
        for j in range(settings.NUMBER_OBJECTIVE_AT_OBTIMIZATE): # la lista de objetivos posiblemente se una lita de enteros 
            PopulationServices.order_solution_of_objetive_value(frente, j)
            frente[0].crowding_distance = settings.INFINITE_POSITIVE
            for i in range(1, len(frente)-1):
                value = (frente[i+1].fitness[j] - frente[i-1].fitness[j])
                if rango[j]!= 0:
                   value = value/rango[j]
                frente[i].crowding_distance += value
            frente[-1].crowding_distance = settings.INFINITE_NEGATIVE
            
    
    def get_range_of_objective(frente: List[Solution]) -> List[int]:
        # para cada objetivo se calcula el max y el mix y se guarda el rango (max- min)
        # return list rangos, max y min por objetivo [[max-minx],[max,min]..]
        rango: List[int] = []
        min = settings.INFINITE_POSITIVE
        max = settings.INFINITE_NEGATIVE
        for index_objective in range(settings.NUM_OBJECTIVE):
            for solution in frente:
                if min > solution.fitness[index_objective]:
                    min = solution.fitness[index_objective]
                if max < solution.fitness[index_objective]:
                    max = solution.fitness[index_objective]
            rango.append(max-min)
        return rango
            
    @staticmethod
    def get_solution_of_range(population: Population, range: int, index_solution: int):
        solution = population.get_Solutions_of_range(range)
        if solution:
            return solution[index_solution]
        else:
            return solution
        

    @staticmethod
    def order_solution_of_objetive_value(frente, index_objective):
        result = sorted(frente, key = lambda solution : solution.fitness[index_objective], reverse=True) # reserve = True: ordena descendente
        return result

    
        

