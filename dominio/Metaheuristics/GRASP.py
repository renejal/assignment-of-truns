import copy
from dominio.Algorithm import Algorithm
from dominio.Solution import Solution
from dominio.vigilant_assigment import VigilantAssigment
from services.tweak_service import Tweak_service

class Grasp(Algorithm):
    ALEATORY:int = 0
    CURRENT_EFOS: int = 0
    MAX_EFOS: int = 10
    COMPONENTS_AMOUNT: int = 300
    RESTRICTED_LIST_AMOUNT_COMPONENT:int = 15
    TWEAK_AMOUNT_REPETITIONS: int = 3

    def Execute(self, problem: VigilantAssigment):
        Best = None
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
            for tweak_index in range(self.TWEAK_AMOUNT_REPETITIONS):
                new_solution:Solution = Tweak_service().Tweak(copy.copy(S))
                if new_solution.total_fitness < S.total_fitness:
                    S = new_solution
            if Best == None or S.total_fitness < Best.total_fitness:
                Best = S
            self.CURRENT_EFOS+=1
            print("Nueva  iteracion")
        print(Best.total_fitness)
        print(Best.distance_fitness)
        print(Best.assigned_vigilantes_fitness)
        return Best





