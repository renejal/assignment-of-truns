from typing import List


class Site:
    __site_id: int
    minimum_shift_hours_if_is_special_site: int 

    def __init__(self, site_id : int , minimum_shift_hours_if_is_special_site : int, working_day_start_time : int , weeks_schedule : List[any] ) -> None:
        self.__site_id = site_id