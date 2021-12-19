from typing import List
import numpy as np
import math
#from dominio.Shift import Shift

class Vigilant3:

    __vigilant_id : int
    __expected_place_to_work: int
    __distances_between_places_to_work: List[int]
    __hours_worked: int 
    __hours_worked_by_week: List[int] 
  #  __shifts : List[Shift]

    def __init__(self, vigilant_id : int , expected_place_to_work : int , distances_between_places_to_work : List[int], total_weeks) -> None:
        self.__vigilant_id = id
        self.__expected_place_to_work = expected_place_to_work
        self.__distances_between_places_to_work = distances_between_places_to_work
        self.__hours_worked = 0
        self.__hours_worked_by_week = np.zeros(total_weeks)

    
    def setHoursWorked(self,week):
        self.HoursWeeks[week] = self.HoursWeeks[week]+1
        self.HoursWorked+=1
   
    def setShift(self, period, site):
        self.shifts[period] = site
    
    def setShifts(self,shifts,site):
        for period in range(shifts[0],shifts[1]+1):
            self.setShift(period,site)