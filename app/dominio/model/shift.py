from typing import List

class Shift:
    id: int
    shift_start: int
    shift_end: int
    necesary_vigilantes: int
    assigment_vigilantes: List[int]

    def __init__(self,id, shift_start: int, shift_end: int, necesary_vigilantes: int) -> None:
        self.id = id
        self.shift_start = shift_start
        self.shift_end = shift_end
        self.necesary_vigilantes = necesary_vigilantes
        self.assigment_vigilantes = []

    def add_vigilant(self, vigilant_id: int):
        self.assigment_vigilantes.append(vigilant_id)

    def change_vigilant(self, id_last_vigilant, id_new_vigilant):
        if id_last_vigilant in self.assigment_vigilantes:
            self.assigment_vigilantes.remove(id_last_vigilant)  
        self.assigment_vigilantes.append(id_new_vigilant)
