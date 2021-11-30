import dataclasses
from typing import Dict, List
from utils.dataclass_classmethod import FromDictMixin
from dominio.model.week import Week

@dataclasses.dataclass
class Site(FromDictMixin):
    description: str = ""
    id: int = 0
    is_special_site: bool = False
    working_day_start_time: int = 0
    weeks_schedule: List[Week] = dataclasses.field(default_factory=list)