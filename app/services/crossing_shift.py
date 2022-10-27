import copy
from typing import List
from utils.order import Order
from dominio.model.shift import Shift
from utils import aleatory
from utils import union
from dominio.Solution import Solution
from dominio.Component import Component
from dominio.population import Population
from services.crossing import Crossing
from conf import settings
class CrossingShift:


    @classmethod
    def crossing_hours_extras(self, population:  List[Solution], objective_index=1):
        """ese cruce intercambia jornadas laborales entre los padres teniendo en cuenta el  
        objetivo mejoramiento horas extras"""
        solution_A, solution_B = Crossing.get_parents_by_objetive(population, objective_index, settings)
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
        solution_A, solution_B = Crossing.get_parents_by_objetive(population, objective_index, settings)
        childs = []
        child = self.exchange_shift(copy.copy(solution_A), copy.copy(solution_B))
        childs.append(child)
        child = self.exchange_shift(copy.copy(solution_B),copy.copy(solution_A))
        childs.append(child)
        return childs

    @classmethod
    def crossing_vigilant_assigment(self, population: Population , objective_index=3):
        childrens = []
        childrens.append(self.crossing_vigilant(population, objective_index))
        childrens.append(self.crossing_vigilant(population, objective_index))
        return childrens

    @classmethod
    def crossing_vigilant(self, population: Population , objective_index):
        """crossing enfocado en asignar vigilantes al sitio cuando los vigilantes superan el numero de horas normal
            ordinaria

        Args:
            population (List[Solution]): poblacion de soluciones a tener en cuenta para el cruce
            objective_index (int, optional): objetivo a obtimizar

        Returns:
            Dos hijos resultantes del cruce entre los dos padres
        """
        parent_one = Crossing.get_best_parent(population.populations, objective_index)
        bad_gen_parent_one = parent_one.get_bad_by_fitnnes("necesary_vigilantes") # esto con el fin de mejorar el gen que menos aporta a la solucion #todo: poner rando en lista restringida
        value = self.get_gen_best_whit_list_restricted(bad_gen_parent_one, population,"necesary_vigilantes")
        parent_two: Solution = population.get_solution_whit_id_soluction(value[0]["id_soluction"])
        best_gen_parent_two = parent_two.get_gen(value[0]["id_gen"])
        parent_one.crossing_gen(bad_gen_parent_one,best_gen_parent_two)
        temp_fitnnes = parent_one.total_fitness
        parent_one.calculate_fitness()
        print(f"parent_one id: {parent_one.id} parent_two: id: {parent_two.id} :fitnnes de {temp_fitnnes} a {parent_one.total_fitness} ")
        return parent_one
    

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
    def get_gen_best_whit_list_restricted(self, gen_to_comparate: Component, population: Population, objective_fitnnes):
        """ obtiene gen ordenada por la ponderacion del fitnes y la similitud al gen_to_comparate
        la busqueda se hace en toda la poblacion para identificar que gen de que sonlucion puede aportar mejor fitnnes
             0 = similitud 100%
        Args:
            gen_to_comparate (Componente): gen con el cual se va a comparar 
            gen (Componente): gen para validar su similitud  
        Returns:
            list: mejor gen encontrado de una lista restringidad en base a su militud con "gen_to_comparate" y el fitnnes
        """
        # 1. contar la hora de inicio y finalizacion de cada workign_day, ademas del numero de vigialantes 
        simility_list = []
        gen_to_comparate.order_workings_days()
        for soluction in population.populations:
            for gen in soluction.sites_schedule:
                fitnnes_count = 0 # conteo de fitnes del gen
                simility_count = 0 # conteo del grado de similitud del gen
                gen.order_workings_days()
                for shift_to_comparate_copy, shift in zip(gen_to_comparate.site_schedule, gen.site_schedule):
                    if shift_to_comparate_copy.shift_start != shift.shift_start:
                        simility_count +=1
                    if shift_to_comparate_copy.shift_end != shift.shift_end:
                        simility_count +=1
                    if shift_to_comparate_copy.necesary_vigilantes != shift.necesary_vigilantes: 
                        simility_count +=1

            fitnnes = gen.get_fitness_by_criteria(objective_fitnnes),
            # print(f"""idsoluction: {soluction.id} id gen: {gen.site_id} 
            #       simility: {simility_count}, fitnnes {fitnnes[0]} 
            #       fitness_simility {fitnnes[0] + simility_count}""")
            simility_list.append({"id_soluction":soluction.id,
                                    "id_gen":gen.site_id,
                                    "simility": simility_count,
                                    "fitnnes": fitnnes[0],
                                    "fitnnes_simility": fitnnes[0] + simility_count
                                    })
        simility_list = sorted(simility_list, key= lambda gen: gen.get("fitnnes_simility"), reverse=False)
        value = Order.list_restricted(simility_list,1,settings.NUM_PARENTS_OF_ORDERED_POPULATION)
        return value

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

        
