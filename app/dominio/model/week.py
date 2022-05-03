from utils.dataclass_classmethod import FromDictMixin
import dataclasses
from dominio.model.day import Day
from typing import List

@dataclasses.dataclass
class Week(FromDictMixin):
    description: str = ""
    days: List[Day] = dataclasses.field(default_factory=list)