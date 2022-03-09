import copy
import random

from dominio.Algorithm import Algorithm
from dominio.Solution import Solution
from dominio.vigilant_assigment import VigilantAssigment
from services.tweak_service import Tweak_service
from utils.graph import Graph

class Grasp(Algorithm):
    ALEATORY:int = 0
    CURRENT_EFOS: int = 0
    MAX_EFOS: int = 30
    # COMPONENTS_AMOUNT: int = 300
    COMPONENTS_AMOUNT: int = 150
    # RESTRICTED_LIST_AMOUNT_COMPONENT:int = 15
    RESTRICTED_LIST_AMOUNT_COMPONENT:int = 15
    TWEAK_AMOUNT_REPETITIONS: int = 70

    def Execute(self, problem: VigilantAssigment):
        Best = None
        data = []
        while self.CURRENT_EFOS < self.MAX_EFOS:
            S = Solution(problem, self.ALEATORY)
            i  = 1
            while S.is_solution_complete():
                components = S.create_components(self.COMPONENTS_AMOUNT)
                restricted_list = components
                i+=1
                if restricted_list == None:
                    continue
                else:
                    best_restricted_list = S.get_best_components(restricted_list,self.RESTRICTED_LIST_AMOUNT_COMPONENT)
                    S.merge_component(best_restricted_list)    
            data.append([S.missing_shifts_fitness,S.assigned_vigilantes_fitness,S.extra_hours_fitness,S.distance_fitness,self.CURRENT_EFOS+1,1])               
            for tweak_index in range(self.TWEAK_AMOUNT_REPETITIONS):
                tweak = random.randint(1,4)      
                new_solution:Solution = Tweak_service().Tweak(copy.deepcopy(S),tweak)
                if new_solution.fitness[tweak-1] < S.fitness[tweak-1]:
                    S = new_solution
                data.append([new_solution.missing_shifts_fitness,new_solution.assigned_vigilantes_fitness,new_solution.extra_hours_fitness,new_solution.distance_fitness,self.CURRENT_EFOS+1,tweak_index+1])               
            if Best == None or S.total_fitness < Best.total_fitness:
                Best = S
            self.CURRENT_EFOS+=1
            print("Nueva  iteracion")
        
        Graph(data)
        print("total:" + str(Best.total_fitness))
        print("Missinig shifts:" + str(Best.missing_shifts_fitness))
        print("Extra hours:" + str(Best.extra_hours_fitness))
        print("Amount Vigilants:" + str(Best.assigned_vigilantes_fitness))
        print("Distance:" + str(Best.distance_fitness))
        return Best





