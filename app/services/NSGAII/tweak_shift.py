from turtle import right
from typing import List
from scipy.fftpack import shift
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
        # calcular los inner, left , ringt
        #lista de working 
        schedules = component_b.site_schedule
        self.add_new_working_day(schedules, working_day)


    def add_new_working_day(schedule: List[shift], working_day: shift):
        A = working_day
        workigns = []
        assigemend_working = False
        i = 0
        while i < len(schedule):
            left, inner, right = union.calculate(A, schedule[i])
            temp = union.convert_continue(A)
            if left == [] and inner != [] and right == [] :
                continue
            if left != [] and inner == [] and right != [] :
                "caso 1: todo a esta dentro de b"
                workigns.append(left + inner)
                assigemend_working = True
                A = left
                continue
            if left != [] and inner != [] and right != [] and assigemend_working:
                "caso 1.1: todo B esta en A2 y assigment workig = true"
                workigns.append(right)
                break
            if left == [] and inner != [] and right != [] and not assigemend_working:
                "caso 2: todo B esta en A0 y assigment workig = False"
                workigns.append(left)
                assigemend_working = True
                A = right
                continue
            if left == [] and inner != [] and right != [] and assigemend_working:
                "caso 2.1: todo B esta en A0 y assigment workig = True"
                workigns.append(right)
                break
            if left != [] and inner != [] and right == [] and not assigemend_working:
                "caso 3: todo A0 esta dentro de B assigment working = False"
                workigns.append(left + inner)
                assigemend_working = True
                A = left
                continue
            if left == [] and inner != [] and right != [] and assigemend_working:
                "caso 3.1: todo b esta dentro de a2 y assigmet working = True" 
                workigns.append(left)
                break
            if left != [] and inner != [] and right != [] and not assigemend_working:
                "caso 4: assigmet working = false" 
                workigns.append(right)
                workigns.append(left + inner)
                A = left + inner
                assigemend_working = True # lo que esta en left y inner ya se ha asignado
                continue
            if left != [] and inner != [] and right == [] and assigemend_working:
                "caso 4.1: todo A0 esta dentro de B assigment working = True"
                A = left # lo que esta en left y inner ya se ha asignado tomamos solo lo que esta en left para coparar con la siguiente working day
                continue
            ## caos 5 validar que la nueva jornada ti pueda se ingresar esto se puede evidenciar si no hay

        
