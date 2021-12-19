import dataclasses
from typing import List
from utils.dataclass_classmethod import FromDictMixin



@dataclasses.dataclass
class Vigilant(FromDictMixin):
    id: int = 0
    default_place_to_look_out: int = -1
    distance: List[int] = dataclasses.field(default_factory=list)
    # shifts : List[Shift] = []

    # def assign_shift(self,shift):
    #     self.shifts.append(shift)





