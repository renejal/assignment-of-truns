import dataclasses
import math
from typing import List
from utils.dataclass_classmethod import FromDictMixin
from dominio.model.week import Week

@dataclasses.dataclass
class Site(FromDictMixin):
    description: str = ""
    id: int = 0
    total_weeks: int = 0
    is_special_site: bool = False
    weeks_schedule: List[Week] = dataclasses.field(default_factory=list)
    total_missing_shifts = 0
    minimum_necessary_vigilantes = 0
    max_extra_hours = 0

    def calculate_max_extra_hours(self):
        max_extra_hours = 0
        for week_schedule in self.weeks_schedule:
            hours_to_work_on_week = 0.0
            for day in week_schedule.days:
                for working_day in day.working_day:
                     hours_to_work_on_week += (working_day.working_end - working_day.working_start + 1)*working_day.num_vigilantes
            max_extra_hours+= math.floor(hours_to_work_on_week/(49*math.ceil(hours_to_work_on_week/56)))
        self.max_extra_hours = max_extra_hours
        