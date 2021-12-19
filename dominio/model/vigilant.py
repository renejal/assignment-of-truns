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
        self._shifts.append(shift)

    def set_total_hours_worked_by_week(self,weeks_amount:int):
        self._total_hours_worked_by_week = [0] * weeks_amount
    # get
    @property
    def id(self):
        return self.id

    @property
    def default_place_to_look_out(self):
        return self._default_place_to_look_out

    @property
    def distance(self):
        return self._distance

    @property
    def shifts(self):
        return self._shifts

    #set
    @default_place_to_look_out.setter
    def default_place_to_look_out(self, default_place_to_look_out):
        self._default_place_to_look_out = default_place_to_look_out

    @distance.setter
    def distance(self, distance):
        self._distance = distance



