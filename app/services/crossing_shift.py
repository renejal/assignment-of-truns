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
        solution_A, solution_B = Crossing.get_parents_by_objetive(population, objective_index)
        childs = []
        child = self.exchange_shift(copy.copy(solution_A), copy.copy(solution_B))
        childs.append(child)
        child = self.exchange_shift(copy.copy(solution_B),copy.copy(solution_A))
        childs.append(child)
        return childs

    @classmethod
    def crossing_missing_shift(self, population:  List[Solution], objective_index=2):
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
        gen = parent.get_bad_by_fitnnes("necesary_vigilantes") # esto con el fin de mejorar el gen que menos aporta a la solucion #todo: poner rando en lista restringida
        #2. tomar un gen equivalente o similar con mejor fitnes de la poblacion en geneneral
        best_gens_list = self.get_list_order_best_gen_similary_of_population(gen, population,"necesary_vigilantes")
        #3. realizar el cruce de genes 
        self.crossing_gen(population, best_gens_list[random.randint(0,len(best_gens_list)-1)])
        #4 reparar genes afectados con criterios de obtimizacion
        # 2 . obtener el mejor vigilante del gen
        # beforeA = solution_A.fitness[3]
        # beforeB =  solution_B.fitness[3]
        # child = self.exchange_shift(copy.copy(solution_A), copy.copy(solution_B))
        # child.calculate_fitness()
        # childs.append(child)
        # child = self.exchange_shift(copy.copy(solution_B),copy.copy(solution_A))
        # child.calculate_fitness()
        # childs.append(child)
        # print(f"fitnnes A before {beforeA} -fater: {solution_A.fitness[3]}")
        # print(f"fitnnes B before {beforeB} -fater: {solution_B.fitness[3]}")
        # return childs
        pass

    def crossing_gen(self, gen_new:Component, gen_to_change_dict:Dict):
        """realiza el cruce de un gen (gen new id) por (gen to change)

        Args:
            gen_new (Component): gen nuevo que se obtubo como mejor para reemplazar 
            gen_to_change_id (Dict): gen a reemplazar
        """
        gen_to_change_id = random.choice(list(gen_to_change_dict.items()))
        print(gen_to_change_dict)
        get_to_change = random.shuffle(gen_to_change_dict)
        get_to_change = gen_new # se realiza el intercambio
        #1 , se procede al proced

    @staticmethod
    def get_list_order_best_gen_similary_of_population(gen_to_comparate: Component, population: List[Solution], objective_fitnnes):
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

        
