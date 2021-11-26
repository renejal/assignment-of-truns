import dataclasses
from typing import Dict, List
from dominio.site import Site
from dominio.vigilant import vigilant
from utils.dataclass_classmethod import FromDictMixin

@dataclasses.dataclass
class DataSites(FromDictMixin):
    data_sites: List[Site] = dataclasses.field(default_factory=list)

@dataclasses.dataclass
class DataVigilantes(FromDictMixin):
    data_vigilantes: List[vigilant] = dataclasses.field(default_factory=list)