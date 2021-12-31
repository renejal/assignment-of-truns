import dataclasses
from typing import Any, List
from dominio.model.shift import Shift
from utils.dataclass_classmethod import FromDictMixin

@dataclasses.dataclass
class Vigilant(FromDictMixin):
    id: int = 0
    default_place_to_look_out: int = -1
    distances: List[int] = dataclasses.field(default_factory=list)
    shifts:  List[Shift] = dataclasses.field(default_factory=list)
    total_hours_worked: int = 0
    total_hours_worked_by_week: List[int] = dataclasses.field(default_factory=list)
    closet_place: int = -1

    def assign_shift(self, shift: Shift) -> None:
        self.shifts.append(shift)

    def set_total_hours_worked_by_week(self, weeks_amount:int):
        self.total_hours_worked_by_week = [0] * weeks_amount




