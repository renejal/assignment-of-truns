from dominio.model.shift import Shift
from dominio.model.vigilant import Vigilant
import pytest
from services.vigilant_assigment_service import Vigilant_assigment_service

@pytest.mark.parametrize("site_id,shifts",[
    (
      1,
      [
          Shift(54, 62, 0),
          Shift(63, 71, 0),
      ]
    ),
])
# def get_necesary_vigilants_by_period_in_a_week
def test_get_possible_vigilant_to_assign(site_id,shifts):
    pass

@pytest.mark.parametrize("vigilant,shift,expected"[
    (
      Vigilant(0,0,[],[],0,[0,0]),
      Shift(6,13),
      True
    ),
])
def should_check_if_vigilant_is_available_correctly(vigilant:Vigilant, shift: Shift, expected):
    assert Vigilant_assigment_service.is_vigilant_avaible(Vigilant_assigment_service,vigilant,shift) == expected

