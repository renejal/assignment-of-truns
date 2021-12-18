from dominio.model.shift import Shift
import pytest

@pytest.mark.parametrize("site_id,shifts",[
    (
      1,
      [
          Shift(54, 62, 0),
          Shift(63, 71, 0),
      ]
    ),
])
def get_necesary_vigilants_by_period_in_a_week
def test_get_possible_vigilant_to_assign(site_id,shifts):
    pass

