from typing import List
from dominio.model.week import Week 


class Site:
    __descripion: str
    __site_id: int
    __minimum_shift_hours_if_is_special_site: int
    __weeks_schedule: List[Week]


    def __init__(self, site_id : int , minimum_shift_hours_if_is_special_site : int, working_day_start_time : int , weeks_schedule : List[Week] ) -> None:
        self.__site_id = site_id
        self.__minimum_shift_hours_if_is_special_site = minimum_shift_hours_if_is_special_site
        self.__working_day_start_time = working_day_start_time
        self.__weeks_schedule = weeks_schedule