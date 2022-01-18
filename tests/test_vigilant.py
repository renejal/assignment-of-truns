from typing import List
import pytest
from dominio.model.vigilant import Vigilant
from dominio.model.shift import Shift


@pytest.mark.parametrize("vigilant, shift, expected",[
    (
        Vigilant(0,-1,[],[],0,[40,0],-1),
        Shift(0,7,3),
        [48,0]
    ),
    (
        Vigilant(0,-1,[],[],0,[40,40],-1),
        Shift(166,173,3),
        [42,46]
    ),
    (
        Vigilant(0,-1,[],[],0,[0,0],-1),
        Shift(164,173,3),
        [4,6]
    )
])
def test_should_assing_hours_correctly(vigilant: Vigilant, shift:Shift, expected: List[int]):
    vigilant.assing_hours_worked(shift)
    assert vigilant.total_hours_worked_by_week == expected
