from utils import union
from dominio.model.shift_place import Shift_place
from dominio.model.shift import Shift
from conf.settings import DISTANCE_FITNESS_VALUE, ASSIGNED_VIGILANTES_FITNESS_VALUE, EXTRA_HOURS_FITNESS_VALUE, MISSING_FITNESS_VALUE, MAXIMUM_WORKING_AMOUNT_HOURS_BY_WEEK,CALCULATE_HOURS_FITNESS
from typing import List, Dict
from dominio.model.vigilant import Vigilant

class Component:

    site_id: int
    site_schedule: List[Shift]
    missing_shifts: List[Shift]
    assigned_Vigilantes: Dict[int,Vigilant] 
    
    missing_shifts_fitness: int = 0
    distance_fitness: int = 0
    extra_hours_fitness: int = 0
    assigned_vigilantes_fitness: int = 0
    modified = False
    total_fitness:int = 0
    
    def __init__(self, site_id : int , site_schedule : List[Shift], assigned_vigilantes: List[Vigilant]) -> None:   
        self.site_id = site_id
        self.site_schedule = site_schedule
        self.assigned_Vigilantes = {x.id: x for x in assigned_vigilantes}
        self.missing_shifts = []
        self.calculate_inicial_fitness()
 
    def get_vigilantes(self) -> List[Vigilant]:
        return self.assigned_Vigilantes
    
    def get_vigilant(self, id: int)-> Vigilant:
        for vigilant in self.assigned_Vigilantes:
            if vigilant == id:
                return self.assigned_Vigilantes.get(id) 
    

    def exchange_vigilant(self, id_vigilant_new, id_vigilant_exchange):
        self.get_vigilant(id_vigilant_exchange).set_id(id_vigilant_new)
    
    def get_shift(self, par_shift: Shift):
        for shift in self.site_schedule:
            if (shift.shift_end == par_shift.shift_end and 
                shift.shift_start == par_shift.shift_start):
                return shift
        return None
    
    def clear_shift_vigilant(self, par_vigilant: Vigilant):
        shifts = par_vigilant.shifts
        while shifts:
            shift = shifts.pop(0)
            main_shift = self.get_shift(shift.shift)
            if not main_shift:
                continue
            if par_vigilant.id in main_shift.assigment_vigilantes:
                main_shift.assigment_vigilantes.remove(par_vigilant.id)
        par_vigilant.last_shift = None

    def crossing_shift(self, vigilant_bad: Vigilant, par_vigilant_best: Vigilant):
        """hace un cruce de los shift de los vigilantes, los shit de vigilant_best 
        son pasado al vigilante del objeto actual con id par_vigilant_id

        Args:
            par_vigilant_id (int): id del vigilane al cual se le van a actulizar los shifts
            par_vigilant_best (Vigilant): vigilanstes que contiene los shits best
        """
        try:
            if vigilant_bad and par_vigilant_best:
                self.clear_shift_vigilant(vigilant_bad)
                index_best = 0
                while True:
                    if index_best < len(par_vigilant_best.shifts):
                        # 1. busar shift en site_schedule shift y asignar a vigilants bad
                        shift_best=self.get_shift(par_vigilant_best.shifts[index_best].shift)
                        if not shift_best:
                            index_best += 1
                            continue
                        shift_best.add_vigilant(vigilant_bad.id)
                        vigilant_bad.shifts.append(Shift_place(shift_best,self.site_id))
                    else:
                        break
                    index_best += 1
        except ValueError as e:
            pass


    def add_vigilant(self, vigilant_best: Vigilant):
        "asignar el vigilante al sitio"
        pass
    def delete_vigilant(self, id_vigilant: int):
        "Todo implementar delete o desasignar vigilantes del gen actual"
        if self.assigned_Vigilantes.get(id_vigilant):
            del self.assigned_Vigilantes[id_vigilant]

    def calculate_inicial_fitness(self) -> None:
        self.assigned_vigilantes_fitness = 0
        self.distance_fitness = 0
        self.extra_hours_fitness = 0
        self.missing_shifts_fitness = 0
        self.total_fitness = 0
        for shift in self.site_schedule:
            if shift.necesary_vigilantes != len(shift.assigment_vigilantes):
                self.missing_shifts.append(shift)
                self.missing_shifts_fitness+= MISSING_FITNESS_VALUE*(abs(shift.necesary_vigilantes - len(shift.assigment_vigilantes))) * (shift.shift_end - shift.shift_start + 1)
                self.total_fitness+= MISSING_FITNESS_VALUE*(abs(shift.necesary_vigilantes - len(shift.assigment_vigilantes))) * (shift.shift_end - shift.shift_start + 1)
        if self.assigned_Vigilantes == None:
            return
        for vigilant in self.assigned_Vigilantes.values():

            # if vigilant.default_place_to_look_out !=1 and vigilant.default_place_to_look_out != self.site_id and vigilant.closet_place != self.site_id:
              
            self.distance_fitness+= DISTANCE_FITNESS_VALUE * vigilant.distances[self.site_id - 1]
            self.total_fitness+= DISTANCE_FITNESS_VALUE * vigilant.distances[self.site_id - 1]
            #TODO Revisar si es mejor calcular las horas por semaana si trabajo o algo
            for hour_by_week in vigilant.total_hours_worked_by_week:
                # if index-1 == len(vigilant.total_hours_worked_by_week):
                #     break
                if CALCULATE_HOURS_FITNESS:
                    if hour_by_week > MAXIMUM_WORKING_AMOUNT_HOURS_BY_WEEK:
                        self.extra_hours_fitness += EXTRA_HOURS_FITNESS_VALUE * (hour_by_week - MAXIMUM_WORKING_AMOUNT_HOURS_BY_WEEK)
                        self.total_fitness += EXTRA_HOURS_FITNESS_VALUE * (hour_by_week - MAXIMUM_WORKING_AMOUNT_HOURS_BY_WEEK)
                if hour_by_week < MAXIMUM_WORKING_AMOUNT_HOURS_BY_WEEK and hour_by_week > 0:
                    missing_hours = MAXIMUM_WORKING_AMOUNT_HOURS_BY_WEEK - hour_by_week
                    # if hour_by_week >= MAXIMUM_WORKING_AMOUNT_HOURS_BY_WEEK / 2:
                    #     missing_hours = MAXIMUM_WORKING_AMOUNT_HOURS_BY_WEEK - hour_by_week                        
                    self.assigned_vigilantes_fitness += missing_hours
                    self.total_fitness+= missing_hours
            self.assigned_vigilantes_fitness += ASSIGNED_VIGILANTES_FITNESS_VALUE * len(self.assigned_Vigilantes) 
            self.total_fitness += ASSIGNED_VIGILANTES_FITNESS_VALUE * len(self.assigned_Vigilantes) 

    def get_fitness_by_criteria(self, fitnessToOptimize:str) -> int:
        if fitnessToOptimize == "missing_shifts":
            return self.missing_shifts_fitness
        if fitnessToOptimize == "necesary_vigilantes":
            return self.assigned_vigilantes_fitness
        if fitnessToOptimize == "extra_hours":
            return self.extra_hours_fitness
        if fitnessToOptimize == "distance":
            return self.distance_fitness

    def order_workings_days(self: List[Shift]):
        "ordena los workings days de el componente self"
        for i in range(len(self.site_schedule)):
            temp = i
            for j in range(i+1, len(self.site_schedule)):
                if self.site_schedule[j].shift_start < self.site_schedule[temp].shift_start:
                    temp = j
            self.site_schedule[i], self.site_schedule[temp] = self.site_schedule[temp], self.site_schedule[i]
        self.assigment_id_order()
    
    def assigment_id_order(self):
        pass

    def validate_working_day(self, shift: Shift):
        schedules = self.site_schedule
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
                    
    def add_new_workingday(self, working_day):
        A = working_day
        schedule = self.site_schedule
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

        