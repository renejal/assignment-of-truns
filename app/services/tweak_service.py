import random
from dominio.Solution import Solution
from services.tweak_assignment_vigilantes_amount import Tweak_assignment_vigilantes_amount
from services.tweak_distance import Tweak_distance
from services.tweak_extra_hours import Tweak_extra_hours
from services.tweak_missing_shifts import Tweak_missing_shifts
from conf.settings import MISSING_SHIFT_TWEAK_PROBABILITY, ASSIGNED_VIGILANTES_TWEAK_PROBABILITY, EXTRA_HOURS_TWEAK_PROBABILITY,DISTANCE_TWEAK_PROBABILITY

class Tweak_service:

    tweak_missing_shifts: Tweak_missing_shifts = Tweak_missing_shifts()
    tweak_extra_hours: Tweak_extra_hours = Tweak_extra_hours()
    tweak_assignment_vigilantes_amount: Tweak_assignment_vigilantes_amount = Tweak_assignment_vigilantes_amount()
    tweak_distance: Tweak_distance = Tweak_distance()

    def Tweak(self, solution: Solution):
        tweak = random.choices([1,2,3,4], weights = (MISSING_SHIFT_TWEAK_PROBABILITY,ASSIGNED_VIGILANTES_TWEAK_PROBABILITY,EXTRA_HOURS_TWEAK_PROBABILITY,DISTANCE_TWEAK_PROBABILITY))[0]
        if tweak == 1:
            solution = self.tweak_missing_shifts.missing_shifts_tweak(solution)
        elif tweak == 2:
            solution = self.tweak_assignment_vigilantes_amount.assignment_vigilantes_amount(solution)
        elif tweak == 3:
            solution = self.tweak_extra_hours.extra_hours_tweak(solution)
        else:
            solution = self.tweak_distance.tweak_distance(solution)
        solution.calculate_fitness()
       
        return solution
