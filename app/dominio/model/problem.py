import dataclasses
from typing import List
from dominio.model.site import Site
from dominio.model.vigilant import Vigilant
from utils.dataclass_classmethod import FromDictMixin

@dataclasses.dataclass
class DataSites(FromDictMixin):
    data_sites: List[Site] = dataclasses.field(default_factory=list)

@dataclasses.dataclass
class DataVigilantes(FromDictMixin):
    data_vigilantes: List[Vigilant] = dataclasses.field(default_factory=list)

@dataclasses.dataclass
class DataUser(FromDictMixin):
    id_user: str = dataclasses.field(default_factory=list)

