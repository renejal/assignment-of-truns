from ast import Dict
import dataclasses
import math
from typing import List
from dominio.model.shift import Shift
from dominio.model.shift_place import Shift_place
from utils.dataclass_classmethod import FromDictMixin

@dataclasses.dataclass
class Vigilant(FromDictMixin):
    id: int = 0
    default_place_to_look_out: int = -1
    distances: List[int] = dataclasses.field(default_factory=list)
    shifts: List[Shift_place] = dataclasses.field(default_factory=list)
    sites_to_look_out: dict[int, int] =  dataclasses.field(default_factory=dict)
    total_hours_worked: int = 0
    total_hours_worked_by_week: List[int] = dataclasses.field(default_factory=list)
    closet_place: int = -1
    last_shift: Shift = None

    def assign_shift(self, shift: Shift, site_id: int) -> None:
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


