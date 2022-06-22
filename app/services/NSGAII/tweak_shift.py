from typing import List
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
            print("i",i)
            print(f"A: {union.print_working_day(A)}")
            print(f"B: {union.print_working_day(schedule[i])}")
            left, inner, right = union.calculate(A,schedule[i])
            print("union: ", left, inner, right)
            if left == [] and inner != [] and right == [] :
                print("caso 0")
                pass
            elif left !=[] and inner == [] and right != []:
                print("caso 0.1")
                pass
            elif left != [] and inner != [] and right == [] :
                print("caso 1")
                "caso 1: todo a esta dentro de b"
                working = left + inner 
                schedule[i].shift_start = min(working)
                schedule[i].shift_end = max(working)
                assigemend_working = True
                A = left
                print(f"A:{A}")
                print("----------")
            elif left == [] and inner != [] and right != [] and assigemend_working:
                print("caso 1.1")
                "caso 1.1: todo B esta en A2 y assigment workig = true"
                schedule[i].shift_start = min(right)
                schedule[i].shift_end = max(right)
                break
            elif left == [] and inner != [] and right != [] and not assigemend_working:
                print("caso 2")
                "caso 2: todo B esta en A0 y assigment workig = False" 
                working = inner + right
                schedule[i].shift_start = min(working)
                schedule[i].shift_end = max(right)
                assigemend_working = True
                A = right
                print(f"A:{A}")
                print("----------")
            elif left == [] and inner != [] and right != [] and assigemend_working:
                print("caso 2.1")
                "caso 2.1: todo B esta en A0 y assigment workig = True"
                schedule[i].shift_start = min(right)
                schedule[i].shift_end = max(right)
                print("----------")
                break
            elif left != [] and inner != [] and right == [] and not assigemend_working:
                print("caso 3")
                "caso 3: todo A0 esta dentro de B assigment working = False"
                schedule[i].shift_start = min(left)
                schedule[i].shift_end = max(inner)
                assigemend_working = True
                A = left
                print(f"A:{A}")
                print("----------")
            elif left == [] and inner != [] and right != [] and assigemend_working:
                print("caso 3.1")
                "caso 3.1: todo b esta dentro de a2 y assigmet working = True" 
                schedule[i].shift_start = min(left)
                schedule[i].shift_end = max(right)
                print("----------")
                break
            elif left != [] and inner != [] and right != [] and not assigemend_working:
                print("caso 4")
                "caso 4: assigmet working = false" 
                print("i", i) 
                # schedule.insert(i,Shift(None,min(right),max(right),None))
                schedule[i].shift_start = min(right) 
                schedule[i].shift_end= max(right) 
                schedule[i+1].shift_start = min(inner) # le suma el los valore faltantes a la siguieten working_day
                print("i+1",union.print_working_day(schedule[i+1]))
                assigemend_working = True # lo que esta en left y inner ya se ha asignado
                print("----------")
            elif left != [] and inner != [] and right != [] and assigemend_working:
                print("caso 4.1")
                "caso 4.1: todo A2 esta dentro de B assigment working = True"
                schedule[i].shift_start = min(right)
                schedule[i].shift_end= max(right)
                A = left # lo que esta en left y inner ya se ha asignado tomamos solo lo que esta en left para coparar con la siguiente working day
            ## caos 5 validar que la nueva jornada ti pueda se ingresar esto se puede evidenciar si no hay
            i = i + 1
        return schedule

        
