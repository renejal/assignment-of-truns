from typing import List
from dominio.problem import Problem

class Shift:
    __shift_start: int
    __shift_end: int
    __necesary_vigilants: int 
    __assigment_vigilants: List[Problem]

    def __init__(self,shift_start: int, shift_end: int, necesary_vigilants: int) -> None:
        self.__shift_start = shift_start
        self.__shift_end = shift_end
        self.__necesary_vigilants = necesary_vigilants

    def __addVigilant(self, vigilant: Vigilant):
        self.__assigment_vigilants.append(vigilant) 
