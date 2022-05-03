from utils.dataclass_classmethod import FromDictMixin
import dataclasses
from typing import List
from dominio.model.working_day import workingDay

@dataclasses.dataclass
class Day(FromDictMixin):
    description: str = ""
    id: int = 0
    working_day: List[workingDay] = dataclasses.field(default_factory=list)
