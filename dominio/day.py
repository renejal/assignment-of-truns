from utils.dataclass_classmethod import FromDictMixin
import dataclasses
from typing import List, Dict
from dominio.working_day import workingDay
@dataclasses.dataclass
class Day(FromDictMixin):
    description: str = ""
    working_day: List[workingDay] = dataclasses.field(default_factory=list)
