import dataclasses
from typing import Dict, List
from dominio.site import Site
from utils.dataclass_classmethod import FromDictMixin

@dataclasses.dataclass
class Problem(FromDictMixin):
    problem: List[Site] = dataclasses.field(default_factory=list)
