from typing import List
from dominio.vigilant import Vigilant

class Shift:
    __shift_start: int
    __shift_end: int
    __necesary_vigilantes: int
    __assigment_vigilantes: List[Vigilant]

    def __init__(self,shift_start: int, shift_end: int, necesary_vigilantes: int) -> None:
        self.__shift_start = shift_start
        self.__shift_end = shift_end
        self.__necesary_vigilantes = necesary_vigilantes

    def __addVigilant(self, vigilant: Vigilant):
        self.__assigment_vigilantes.append(vigilant)
