from cgi import print_arguments
import sched
from typing import List
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
    def crossing_hours_extras(self, population:  List[Solution], objective_index=2):
        solution_A, solution_B = Crossing.get_parents_by_objetive(population, objective_index)
        childs = []
        child = self.exchange_shift(copy.copy(solution_A), copy.copy(solution_B))
        childs.append(child)
        child = self.exchange_shift(copy.copy(solution_B),copy.copy(solution_A))
        childs.append(child)
        return childs

    @classmethod
    def exchange_shift(self, soluction_A: Solution, soluction_B: Solution) -> Solution:
        """exchange shift of soluciton A for shift soluction B"""
        list_random = [] 
        for i in range(settings.NUMBER_OF_CHILDREN_FOR_PARENTS):
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

        
