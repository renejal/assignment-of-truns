from typing import List
from dominio.model.vigilant import Vigilant

class Shift:
    shift_start: int
    shift_end: int
    necesary_vigilantes: int
    __assigment_vigilantes: List[Vigilant]

    def __init__(self,shift_start: int, shift_end: int, necesary_vigilantes: int) -> None:
        self.shift_start = shift_start
        self.shift_end = shift_end
        self.necesary_vigilantes = necesary_vigilantes

    def __addVigilant(self, vigilant: Vigilant):
        self.__assigment_vigilantes.append(vigilant)
