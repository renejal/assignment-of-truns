import dataclasses
from utils.dataclass_classmethod import FromDictMixin

@dataclasses.dataclass
class workingDay(FromDictMixin):
    description: str = ""
    working_start: int = 0
    working_end: int = 0
    num_vigilantes: int = 0