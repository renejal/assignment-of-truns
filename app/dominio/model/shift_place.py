from dominio.model.shift import Shift

class Shift_place:
    shift: Shift
    site_id: int
    
    def __init__(self, shift: Shift, site_id: int):
        self.shift = shift
        self.site_id = site_id