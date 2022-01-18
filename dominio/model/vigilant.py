import dataclasses
import math
from typing import Any, Dict, List
from dominio.model.shift import Shift
from utils.dataclass_classmethod import FromDictMixin

@dataclasses.dataclass
class Vigilant(FromDictMixin):
    id: int = 0
    default_place_to_look_out: int = -1
    distances: List[int] = dataclasses.field(default_factory=list)
    shifts: Dict[Shift, int] = dataclasses.field(default_factory=dict)
    sites_to_look_out: List[int] =  dataclasses.field(default_factory=list)
    total_hours_worked: int = 0
    total_hours_worked_by_week: List[int] = dataclasses.field(default_factory=list)
    closet_place: int = -1

    def assign_shift(self, shift: Shift, site_id: int) -> None:
        self.shifts[shift] = site_id
        self.assing_hours_worked(shift)
    
    def assign_site(self, id_site: int) -> None:
        self.sites_to_look_out.append(id_site)

    def assing_hours_worked(self, shift:Shift) -> None:
        self.total_hours_worked = shift.shift_end - shift.shift_start + 1
        start_week_of_shift = math.floor(shift.shift_start/168)
        end_week_of_shift  =  math.floor(shift.shift_end/168)
        if start_week_of_shift == end_week_of_shift:
            self.total_hours_worked_by_week[start_week_of_shift]+= shift.shift_end - shift.shift_start + 1
        else:
            self.total_hours_worked_by_week[start_week_of_shift]+= (168*end_week_of_shift)-shift.shift_start
            self.total_hours_worked_by_week[end_week_of_shift]+= shift.shift_end - (168*end_week_of_shift - 1)

    def set_total_hours_worked_by_week(self, weeks_amount:int):
        self.total_hours_worked_by_week = [0] * weeks_amount

    


