import dataclasses
from typing import Any, List
from dominio.model.shift import Shift
from utils.dataclass_classmethod import FromDictMixin



@dataclasses.dataclass
class Vigilant(FromDictMixin):
    id: int = 0
    default_place_to_look_out: int = -1
    distance: List[int] = dataclasses.field(default_factory=list)
    shifts:  List[Shift] = dataclasses.field(default_factory=list)
    total_hours_worked:int = 0
    total_hours_worked_by_week: List[int] = dataclasses.field(default_factory=list)

    def assign_shift(self, shift) -> None:
        self.shifts.append(shift)


