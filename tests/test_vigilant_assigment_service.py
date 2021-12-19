from dominio.model.shift import Shift
from dominio.model.vigilant import Vigilant
import pytest
from services.vigilant_assigment_service import Vigilant_assigment_service

# @pytest.mark.parametrize("site_id,shifts",[
#     (
#       1,
#       [
#           Shift(54, 62, 0),
#           Shift(63, 71, 0),
#       ]
#     ),
# ])
# def get_necesary_vigilants_by_period_in_a_week
# def test_get_possible_vigilant_to_assign(site_id,shifts):
#     pass
vigilantS = Vigilant_assigment_service()
@pytest.mark.parametrize("vigilant, shift, expected",[
    #No shift case
    (
      Vigilant(0,0,[],[],0,[0,0]),
      Shift(6,13,0),
      True
    ),
    #has have not exceeded the max hours work by week
    (
      Vigilant(0,0,[],[],0,[0,40,0,0]),
      Shift(168,175,0),
      True
    ),
    #has have not exceeded the max hours work on 4 week
    (
      Vigilant(0,0,[],[],0,[0,44,44,0]),
      Shift(332,339,0),
      True
    ),
    #Assingin shift in existing same shift
    (
      Vigilant(0,0,[],[
        Shift(6,13,0)
      ],0,[8,0]),
      Shift(6,13,0),
      False
    ),
    #Doesn has enough time rest to take new shift case initial shift
    (
      Vigilant(0,0,[],[
        Shift(0,5,0)
      ],0,[8,0]),
      Shift(6,13,0),
      False
    )
    #Doesn has enough time rest to take new shift case before new shift
    ,(
      Vigilant(0,0,[],[Shift(152,159,0)],0,[8]),
      Shift(160,167,0),
      False
    ),
    #Doesn has enough time rest to take new shift case after new shift
    (
      Vigilant(0,0,[],[Shift(152,159,0)],0,[8]),
      Shift(140,151,0),
      False
    ),
    #has enought rest time after but not before new shift
    (
      Vigilant(0,0,[],[Shift(100,112,0),Shift(156,167,0)],0,[8]),
      Shift(130,137,0),
      False
    ),
    #has enought rest time before but not after new shift
    (
      Vigilant(0,0,[],[Shift(100,111,0),Shift(155,167,0)],0,[8]),
      Shift(130,137,0),
      False
    ),
    #has enought rest time before and after new shift
    (
      Vigilant(0,0,[],[Shift(100,111,0),Shift(156,165,0)],0,[8]),
      Shift(130,137,0),
      True
    ),
    #has have not exceeded the max hours work by week
    (
      Vigilant(0,0,[],[],0,[40,0]),
      Shift(5,13,0),
      False
    ),
    #has have exceeded the max hours work on second of four weeks
    (
      Vigilant(0,0,[],[],0,[0,44,44,0]),
      Shift(331,339,0),
      False
    ),
     #has have exceeded the max hours work on third of four weeks
    (
      Vigilant(0,0,[],[],0,[0,44,44,0]),
      Shift(332,340,0),
      False
    ),


])
def test_should_check_if_vigilant_is_available_correctly(vigilant:Vigilant, shift: Shift, expected: bool):
    assert vigilantS.is_vigilant_avaible(vigilant,shift) == expected
