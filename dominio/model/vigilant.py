import dataclasses
from typing import List
from utils.dataclass_classmethod import FromDictMixin

@dataclasses.dataclass
class Vigilant(FromDictMixin):
    _id: int = 0
    _default_place_to_look_out: int = -1
    _distance: List[int] = dataclasses.field(default_factory=list)

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

    #set
    @default_place_to_look_out.setter
    def default_place_to_look_out(self, default_place_to_look_out):
        self._default_place_to_look_out = default_place_to_look_out

    @distance.setter
    def distance(self, distance):
        self._distance = distance



