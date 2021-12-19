import dataclasses
from typing import List
from utils.dataclass_classmethod import FromDictMixin
from dominio.model.week import Week

@dataclasses.dataclass
class Site(FromDictMixin):
    _description: str = ""
    _id: int = 0
    _is_special_site: bool = False
    _weeks_schedule: List[Week] = dataclasses.field(default_factory=list)

    # get
    @property
    def description(self):
        return self._description

    @property
    def is_special_site(self):
        return self._is_special_site

    @property
    def weeks_schedule(self):
        return self._weeks_schedule

    @property
    def id(self):
        return self._id
    #set

    @description.setter
    def description(self, description: str):
        self._description = description

    @is_special_site.setter
    def is_special_site(self, is_special_site):
        self._is_special_site = is_special_site

    @weeks_schedule.setter
    def weeks_schedule(self, weeks_schedule):
        self._weeks_schedule = weeks_schedule
