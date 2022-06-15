from typing import List
import pytest
from dominio.model.shift import Shift
from services.NSGAII.tweak_shift import TweakShift



@pytest.mark.parametrize("shifts, new_working_day",
    [(
    [
        Shift(None,1,6,2),
        Shift(None,7,16,2),
        Shift(None,17,25,2),
        Shift(None,26,34,2),
        Shift(None,35,43,2),
        Shift(None,51,60,2)
    ],
        Shift(None,1,9,2)
    )])
def test_exchage_shift(shifts: List[Shift], new_working_day: Shift):
    workings_day = TweakShift().add_new_working_day(shifts, new_working_day)
    for i in workings_day:
        print("working_day")
        print("shift start", i.shift_start)
        print("shift end", i.shift_end)
        print("-----------------")
    # print(workings_day.)
    assert(workings_day is not None)
