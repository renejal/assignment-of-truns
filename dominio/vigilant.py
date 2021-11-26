import dataclasses
from typing import List
from utils.dataclass_classmethod import FromDictMixin
class vigilant(FromDictMixin):
    id: int = 0
    default_place_to_look_out: int = -1
    distance: List[int] = dataclasses.field(default_factory=list)






