from turtle import right
from typing import List
from scipy.fftpack import shift
from dominio.model.shift import Shift
from utils import aleatory
from utils import union
from dominio.Solution import Solution
from dominio.Component import Component
class TweakShift:
    
    @classmethod
    def tweak_shift(self, soluction_A: Solution , Soluction_B: Solution):
        """exchange shift of component
        Args:
            soluction_A :  solution what have the new shift
            Soluction_B :  solution what have the shfit of exchange (new child)
        """
        component_a: Component = soluction_A.get_random_gen([])
        working_day=aleatory.get_object_ramdon_for_list(0,len(component_a.site_schedule)-1, component_a.site_schedule)
        # ordenar component b
        component_b: Component = Soluction_B.get_random_gen([])
        component_b.order_workings_days()
        schedules = component_b.site_schedule
        self.add_new_working_day(schedules, working_day)

    @classmethod     
    def add_new_working_day(self, schedule: List[Shift], working_day: Shift):
        A = working_day
        workigns = [Shift]
        assigemend_working = False
        i = 0
        while i < len(schedule)-1:
            left, inner, right = union.calculate(A,schedule[i])
            print("left", left)
            print("inner", inner)
            print("right", right)
            if left == [] and inner != [] and right == [] :
                continue
            if left != [] and inner != [] and right == [] :
                print("caso 1")
                "caso 1: todo a esta dentro de b"
                working = left + inner 
                schedule[i].shift_start = min(working)
                schedule[i].shift_end = max(working)
                # workigns.append(left + inner)
                assigemend_working = True
                A = left
                continue
            if left == [] and inner != [] and right != [] and assigemend_working:
                print("caso 1.1")
                "caso 1.1: todo B esta en A2 y assigment workig = true"
                schedule[i].shift_start = min(right)
                schedule[i].shift_end = min(right)
                # workigns.append(right)
                break
            if left == [] and inner != [] and right != [] and not assigemend_working:
                print("caso 2")
                "caso 2: todo B esta en A0 y assigment workig = False" 
                schedule[i].shift_start = min(left)
                schedule[i].shift_end = min(left)
                # workigns.append(left)
                assigemend_working = True
                A = right
                continue
            if left == [] and inner != [] and right != [] and assigemend_working:
                print("caso 2.1")
                "caso 2.1: todo B esta en A0 y assigment workig = True"
                schedule[i].shift_start = min(right)
                schedule[i].shift_end = max(right)
                # workigns.append(right)
                break
            if left != [] and inner != [] and right == [] and not assigemend_working:
                print("caso 3")
                "caso 3: todo A0 esta dentro de B assigment working = False"
                schedule[i].shift_start = min(left)
                schedule[i].shift_end = max(inner)
                # workigns.append(left + inner)
                assigemend_working = True
                A = left
                continue
            if left == [] and inner != [] and right != [] and assigemend_working:
                print("caso 3.1")
                "caso 3.1: todo b esta dentro de a2 y assigmet working = True" 
                schedule[i].shift_start = min(left)
                schedule[i].shift_start = max(right)
                # workigns.append(left)
                break
            if left != [] and inner != [] and right != [] and not assigemend_working:
                print("caso 4")
                "caso 4: assigmet working = false" 
                schedule[i].shift_start = min(right)
                schedule[i].shift_start = max(inner)
                # workigns.append(right)
                schedule.insert(i,Shift(None,min(left), max(inner),None)) # todo no se asigan vigilantes en este caso
                # workigns.append(left + inner)
                A = left + inner
                assigemend_working = True # lo que esta en left y inner ya se ha asignado
                continue
            if left != [] and inner != [] and right == [] and assigemend_working:
                print("caso 4.1")
                "caso 4.1: todo A0 esta dentro de B assigment working = True"
                schedule[i].shift_start = min(left)
                schedule[i].shift_end= min(left)
                A = left # lo que esta en left y inner ya se ha asignado tomamos solo lo que esta en left para coparar con la siguiente working day
                continue
            ## caos 5 validar que la nueva jornada ti pueda se ingresar esto se puede evidenciar si no hay
            i = i + 1
        return schedule

        
