from cgi import print_arguments
import random
import sched
from typing import Dict, List
import copy
from pkg_resources import working_set
from dominio.model.shift import Shift
from utils import aleatory
from utils import union
from dominio.Solution import Solution
from dominio.Component import Component
from services.crossing import Crossing
from conf import settings
class CrossingShift:


    @classmethod
    def crossing_hours_extras(self, population:  List[Solution], objective_index=1):
        """ese cruce intercambia jornadas laborales entre los padres teniendo en cuenta el  
        objetivo mejoramiento horas extras"""
        solution_A, solution_B = Crossing.get_parents_by_objetive(population, objective_index)
        childs = []
        child = self.exchange_shift(copy.copy(solution_A), copy.copy(solution_B))
        childs.append(child)
        child = self.exchange_shift(copy.copy(solution_B),copy.copy(solution_A))
        childs.append(child)
        return childs

    @classmethod
    def crossing_missing_shift(self, population:  List[Solution], objective_index=2):
        """ese cruce intercambia jornadas laborales entre los padres teniendo en cuenta el  
        objetivo missing shift"""
        solution_A, solution_B = Crossing.get_parents_by_objetive(population, objective_index)
        childs = []
        child = self.exchange_shift(copy.copy(solution_A), copy.copy(solution_B))
        childs.append(child)
        child = self.exchange_shift(copy.copy(solution_B),copy.copy(solution_A))
        childs.append(child)
        return childs

    @classmethod
    def crossing_vigilant_assigment(self, population:  List[Solution], objective_index=3):
        """crossing enfocado en asignar vigilantes al sitio cuando los vigilantes superan el numero de horas normal
            ordinaria

        Args:
            population (List[Solution]): poblacion de soluciones a tener en cuenta para el cruce
            objective_index (int, optional): objetivo a obtimizar

        Returns:
            Dos hijos resultantes del cruce entre los dos padres
        """
        #1. toma una de las mejores soluciones por facor de rango NUM_PARENTS_OF_ORDERED_POPULATION de la poblacion
        parent = Crossing.get_best_parent(population, objective_index)
        #1. tomar una gen con peor fitness del "parent"
        bad_gen = parent.get_bad_by_fitnnes("necesary_vigilantes") # esto con el fin de mejorar el gen que menos aporta a la solucion #todo: poner rando en lista restringida
        #2. tomar un gen equivalente o similar con mejor fitnes de la poblacion en geneneral
        best_gens_list = self.get_list_order_best_gen_similary_of_population(bad_gen, population,"necesary_vigilantes")
        #2.1 mejor gen random de la lista restringida
        best_gen_list = best_gens_list[random.randint(0,len(best_gens_list)-1)]
        #3. obtiene el gen mejor reportado en la poblacion
        best_gen = self.get_gen_of_dict(best_gen_list, population)
        # 4 realiza el intercambio de gen
        print(f"before crossing: {parent.total_fitness}")
        parent.set_gen(bad_gen.site_id, best_gen)
        parent.calculate_fitness()
        print(f"after crossing: {parent.total_fitness}")
        print("salio")
        return [parent]
        #5 Todo: reparar genes afectados con criterios de obtimizacion

    @classmethod
    def get_gen_of_dict(self,gen_to_change_dict:dict, population):
        best_soluction = self.get_gen_of_population(population, gen_to_change_dict)
        best_gen = best_soluction.get_gen(gen_to_change_dict["id_gen"])
        return best_gen

    @classmethod 
    def get_gen_of_population(self, population: List[Solution], gen_to_change_dict):
        s = None
        for soluction in population:
            if soluction.id == gen_to_change_dict["id_soluction"]:
                s = soluction
                break
        if not soluction:
            raise("No se Encontro solucion")
        return s

    @classmethod
    def get_list_order_best_gen_similary_of_population(self, gen_to_comparate: Component, population: List[Solution], objective_fitnnes):
        """ obtiene lista  ordenada por la ponderacion del fitnes y la similitud al gen_to_comparate
        la busqueda se hace en toda la poblacion para identificar que gen de que sonlucion puede aportar mejor fitnnes
             0 = similitud 100%
        Args:
            gen_to_comparate (Componente): gen con el cual se va a comparar 
            gen (Componente): gen para validar su similitud  
        Returns:
            list: lista ordenadas de los primrso 10  genes que reportarn mejor fitnnes y similitud
        """
        # 1. contar la hora de inicio y finalizacion de cada workign_day, ademas del numero de vigialantes 
        simility_list = []
        gen_to_comparate.order_workings_days()
        for soluction in population:
            for gen in soluction.sites_schedule:
                gen.order_workings_days()
                simility = 0
                for shift_to_comparate_copy, shift in zip(gen_to_comparate.site_schedule, gen.site_schedule):
                    if shift_to_comparate_copy.shift_start != shift.shift_start:
                        simility +=1
                    if shift_to_comparate_copy.shift_end != shift.shift_end:
                        simility +=1
                    fitnnes = gen.get_fitness_by_criteria(objective_fitnnes),
                    simility_list.append({"id_soluction":soluction.id,
                                          "id_gen":gen.site_id,
                                          "simility": simility,
                                          "fitnnes": fitnnes[0],
                                          "fitnnes_simility": fitnnes[0] + simility
                                          })
        simility_list = sorted(simility_list, key= lambda gen: gen.get("fitnnes_simility"), reverse=False)
        if len(simility_list) < 10:
            raise("No hay un numero de genes suficientes")
        return simility_list[0:10]

    @classmethod
    def exchange_shift(self, soluction_A: Solution, soluction_B: Solution) -> Solution:
        """exchange shift of soluciton A for shift soluction B"""
        list_random = [] 
        for i in range(settings.NUMBER_OF_CHILDREN_GENERATE):
            component_a: Component = soluction_A.get_random_gen([])
            random_number = aleatory.get_random_int(0,len(component_a.site_schedule)-1, list_random)
            list_random.append(random_number)
            working_day = component_a.site_schedule[random_number]
            # ordenar component b
            component_b: Component=soluction_B.get_random_gen([])
            component_b.order_workings_days()
            schedules = component_b.site_schedule
            self.add_new_working_day(schedules, working_day)
            self.validate_working_day(schedules, working_day)
            return soluction_B

    @classmethod
    def validate_working_day(self, schedules : List[Shift], shift: Shift):
        """Valida que el tweak shift este realizado de forma correcta
        Args:
            schedules (List[Shift]): _description_
            shift (Shift): _description_
        """
        for i in range(len(schedules)-1):
            if schedules[i].shift_start == shift.shift_start and schedules[i].shift_end == shift.shift_end:
                if i>0:
                    if schedules[i-1].shift_end < schedules[i].shift_end and schedules[i-1].shift_start < schedules[i].shift_start:
                        pass
                    else:
                        raise("error no se relio el tweak de forma correcta")
                if i < len(schedules)-1:
                    if schedules[i+1].shift_end > schedules[i].shift_end and schedules[i+1].shift_start > schedules[i].shift_start:
                        pass
                    else:
                        raise("error no se relio el tweak de forma correcta")
                    
    @classmethod     
    def add_new_working_day(self, schedule: List[Shift], working_day: Shift):
        A = working_day
        workigns = [Shift]
        assigemend_working = False
        i = 0
        while i < len(schedule)-1:
            left, inner, right = union.calculate(A,schedule[i])
            if left == [] and inner != [] and right == [] :
                pass
            elif left !=[] and inner == [] and right != []:
                pass
            elif left != [] and inner != [] and right == [] :
                working = left + inner 
                schedule[i].shift_start = min(working)
                schedule[i].shift_end = max(working)
                assigemend_working = True
                A = left
            elif left == [] and inner != [] and right != [] and assigemend_working:
                schedule[i].shift_start = min(right)
                schedule[i].shift_end = max(right)
                break
            elif left == [] and inner != [] and right != [] and not assigemend_working:
                working = inner + right
                schedule[i].shift_start = min(working)
                schedule[i].shift_end = max(right)
                assigemend_working = True
                A = right
            elif left == [] and inner != [] and right != [] and assigemend_working:
                schedule[i].shift_start = min(right)
                schedule[i].shift_end = max(right)
                break
            elif left != [] and inner != [] and right == [] and not assigemend_working:
                schedule[i].shift_start = min(left)
                schedule[i].shift_end = max(inner)
                assigemend_working = True
                A = left
            elif left == [] and inner != [] and right != [] and assigemend_working:
                schedule[i].shift_start = min(left)
                schedule[i].shift_end = max(right)
                break
            elif left != [] and inner != [] and right != [] and not assigemend_working:
                schedule[i].shift_start = min(right) 
                schedule[i].shift_end= max(right) 
                schedule[i+1].shift_start = min(inner) # le suma el los valore faltantes a la siguieten working_day
                assigemend_working = True # lo que esta en left y inner ya se ha asignado
            elif left != [] and inner != [] and right != [] and assigemend_working:
                schedule[i].shift_start = min(right)
                schedule[i].shift_end= max(right)
                A = left # lo que esta en left y inner ya se ha asignado tomamos solo lo que esta en left para coparar con la siguiente working day
            ## caos 5 validar que la nueva jornada ti pueda se ingresar esto se puede evidenciar si no hay
            i = i + 1
        return schedule

        
