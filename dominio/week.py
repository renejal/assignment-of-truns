from utils.dataclass_classmethod import FromDictMixin
import dataclasses
from dominio.day import Day
from typing import List, Dict

@dataclasses.dataclass
class Week(FromDictMixin):
    description: str = ""
    days: List[Day] = dataclasses.field(default_factory=list)