import dataclasses
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
    hours_extra_last_week: int = 0
    initial_hour: int = 0
    total_missing_shifts = 0
    minimum_necessary_vigilantes = 0
    hours_to_work_by_week : List[int] = dataclasses.field(default_factory=list)

    def calculate_hours_to_work_by_week(self):
        hours_to_work_by_week = []
        for week_index,week_schedule in enumerate(self.weeks_schedule):
            hours_to_work_on_week = 0.0
            for day in week_schedule.days:
                for working_day in day.working_day:
                     hours_to_work_on_week += (working_day.working_end - working_day.working_start + 1)*working_day.num_vigilantes
                     if self.hours_extra_last_week != 0 and (week_index == 0 or week_index +1 == self.total_weeks ):
                        if working_day.working_end == 23 and day.id == 6:
                            hours_to_work_on_week += self.hours_extra_last_week*working_day.num_vigilantes 
            hours_to_work_by_week.append(hours_to_work_on_week)
        self.hours_to_work_by_week = hours_to_work_by_week
        