from typing import List

class Shift:
    shift_start: int
    shift_end: int
    necesary_vigilantes: int
    assigment_vigilantes: List[int]

    def __init__(self, shift_start: int, shift_end: int, necesary_vigilantes: int) -> None:
        self.shift_start = shift_start
        self.shift_end = shift_end
        self.necesary_vigilantes = necesary_vigilantes

    def add_vigilant(self, id_vigilant: int):
        #self.assigment_vigilantes.append(vigilant)
        pass
