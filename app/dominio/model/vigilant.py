from ast import Dict
import dataclasses
import math
from typing import List, Dict
from dominio.model.shift import Shift
from dominio.model.shift_place import Shift_place
from utils.dataclass_classmethod import FromDictMixin

@dataclasses.dataclass
class Vigilant(FromDictMixin):
    id: int = 0
    default_place_to_look_out: int = -1
    distances: List[int] = dataclasses.field(default_factory=list)
    shifts: List[Shift_place] = dataclasses.field(default_factory=list)
    sites_to_look_out: Dict[int, int] = dataclasses.field(default_factory=dict)
    total_hours_worked: int = 0
    total_hours_worked_by_week: List[int] = dataclasses.field(default_factory=list)
    closet_place: int = -1
    last_shift: Shift = None
    order_distances: Dict[int,int] =  dataclasses.field(default_factory=dict)
    is_assigned: bool = False
    is_usuable: bool = True

    def assign_shift(self, shift: Shift, site_id: int) -> None:
        self.is_assigned = True
        if site_id not in self.sites_to_look_out:
            self.sites_to_look_out[site_id] = 0
        self.sites_to_look_out[site_id] += 1
        self.assing_hours_worked(shift)
        if self.last_shift!= None and shift.shift_start < self.last_shift.shift_end:
            for index,shift_place in enumerate(self.shifts):
                if shift.shift_end < shift_place.shift.shift_start:
                    self.shifts.insert(index,Shift_place(shift,site_id)) 
                    return
        self.shifts.append(Shift_place(shift,site_id))
        self.last_shift = shift

        total_weeks = len(self.total_hours_worked_by_week)
        if total_weeks > 1 and self.total_hours_worked >= ( total_weeks * 48 )/2:
            self.is_usuable = False
            return
        if total_weeks == 1 and self.total_hours_worked >= 48:
            self.is_usuable = False
        
    
    def assing_hours_worked(self, shift:Shift) -> None:
        self.total_hours_worked += shift.shift_end - shift.shift_start + 1
        start_week_of_shift = math.floor(shift.shift_start/168)
        end_week_of_shift  =  math.floor(shift.shift_end/168)
        if start_week_of_shift == end_week_of_shift:
            self.total_hours_worked_by_week[start_week_of_shift]+= shift.shift_end - shift.shift_start + 1
        else:
            self.total_hours_worked_by_week[start_week_of_shift]+= (168*end_week_of_shift)-shift.shift_start
            self.total_hours_worked_by_week[end_week_of_shift]+= shift.shift_end - (168*end_week_of_shift - 1)
    
    def delete_hours_worked(self, shift:Shift) -> None:
        self.total_hours_worked -= shift.shift_end - shift.shift_start + 1
        start_week_of_shift = math.floor(shift.shift_start/168)
        end_week_of_shift  =  math.floor(shift.shift_end/168)
        if start_week_of_shift == end_week_of_shift:
            self.total_hours_worked_by_week[start_week_of_shift]-= shift.shift_end - shift.shift_start + 1
        else:
            self.total_hours_worked_by_week[start_week_of_shift]-= (168*end_week_of_shift)-shift.shift_start
            self.total_hours_worked_by_week[end_week_of_shift]-= shift.shift_end - (168*end_week_of_shift - 1)

    def set_total_hours_worked_by_week(self, weeks_amount:int):
        self.total_hours_worked_by_week = [0] * weeks_amount
        
    def get_shifts_on_week(self,week) -> List[Shift_place]:
        shifts_on_week = []
        for shift in self.shifts:
            actual_week = int(shift.shift.shift_start/168)+1
            if actual_week > week:
                return shifts_on_week
            if actual_week == week:
                shifts_on_week.append(shift)
        return shifts_on_week
    
    def remove_shift(self, shift: Shift_place):
        self.delete_hours_worked(shift.shift)
        self.shifts.remove(shift)
        self.sites_to_look_out[shift.site_id] -= 1
        if self.sites_to_look_out[shift.site_id] == 0:
            del self.sites_to_look_out[shift.site_id]
        if len(self.shifts) == 0:
            self.is_assigned = False

    def set_order_sites_by_distance(self):
        order_sites_by_distance = sorted(range(len(self.distances)), key=lambda k: self.distances[k])
        for index, order_site in enumerate(order_sites_by_distance):
            self.order_distances[order_site+1] = index

    def get_index_sites_by_distance(self):
        return sorted(range(len(self.distances)), key=lambda k: self.distances[k])

    def get_shifts_by_site(self) -> Dict[int,List[Shift]]:
        shifts_by_site: dict[int,List[Shift]] = {}
        for shift in self.shifts:
            if shift.site_id in shifts_by_site:
                shifts_by_site[shift.site_id].append(shift.shift)
            else:
                shifts_by_site[shift.site_id] = [shift.shift]
        return shifts_by_site
        
    def find_shift_place(self, shift:Shift):
        for shift_place in self.shifts:
            if shift_place.shift == shift:
                return shift_place
        return None

    def set_id(self, id):
        self.id = id

