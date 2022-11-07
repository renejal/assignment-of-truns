from utils import aleatory
class Order:
    @classmethod
    def order_solution_of_objetive_value(self,population, index_objective, par_reverse=True):
        result = sorted(population, key = lambda solution : solution.fitness[index_objective], reverse=par_reverse) # reserve = True: ordena descendente
        return result

    @classmethod
    def order_sitio_of_objective_value(self, components, fitnessToOptimize, par_reverse=True):
        result = sorted(components, key = lambda component : component.get_fitness_by_criteria(fitnessToOptimize), reverse=par_reverse) # reserve = True: ordena descendente
        if not result:
            raise("no se encontro genes")
        return result
    
    @ classmethod
    def list_restricted(self, list, num_return, persentage):
        "resive una lista ordenada y dependiendo del paramero NUM_PARENTS_OF_ORDERED_POPULATION retorna uno o mas valores"
        range_best_soluction = int(len(list)* persentage)
        result_list = []
        ramdon_list = []
        for i in range(num_return):
            if range_best_soluction != 0:
                random_number = aleatory.get_random_int(0,range_best_soluction-1,ramdon_list)
                result_list.append(list[random_number])
            else:
                result_list.append(list[0])
                break
            ramdon_list.append(random_number)
        if not result_list:
            raise("no se encontro dato en lista restringidad")
        return result_list
