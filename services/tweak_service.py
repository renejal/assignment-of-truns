from dominio.Solution import Solution
from services.tweak_assignment_vigilantes_amount import Tweak_assignment_vigilantes_amount
from services.tweak_extra_hours import Tweak_extra_hours
from services.tweak_missing_shifts import Tweak_missing_shifts

class Tweak_service:

    tweak_missing_shifts: Tweak_missing_shifts = Tweak_missing_shifts()
    tweak_extra_hours: Tweak_extra_hours = Tweak_extra_hours()
    tweak_assignment_vigilantes_amount: Tweak_assignment_vigilantes_amount = Tweak_assignment_vigilantes_amount()

    def Tweak(self, solution: Solution):
        solution = self.tweak_missing_shifts.missing_shifts_tweak(solution) 
        solution = self.tweak_extra_hours.extra_hours_tweak(solution)
        solution = self.tweak_assignment_vigilantes_amount.assignment_vigilantes_amount(solution)
        #TODO tweak distance
        solution.calculate_fitness()
        return solution