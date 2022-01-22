from typing import List
from unittest import mock
from dominio.model.shift import Shift
from dominio.model.shift_place import Shift_place
from dominio.model.vigilant import Vigilant
import pytest
from services.vigilant_assigment_service import Vigilant_assigment_service
from dominio.vigilant_assigment import VigilantAssigment

vigilantService = Vigilant_assigment_service(VigilantAssigment)

@pytest.mark.parametrize("vigilant, shift, expected",[
    #has have not exceeded the max hours work by week
    (
      Vigilant(0,0,[],[],[],0,[0,40,0,0],0),
      Shift(168,175,0),
      True
    ),
    #has have not exceeded the max hours work on 4 week
    (
      Vigilant(0,0,[],[],[],0,[0,44,44,0],0),
      Shift(332,339,0),
      True
    ),
    #has have not exceeded the max hours work by week
    (
      Vigilant(0,0,[],[],[],0,[40,0],0),
      Shift(5,13,0),
      False
    ),
    #has have exceeded the max hours work on second of four weeks
    (
      Vigilant(0,0,[],[],[],0,[0,44,44,0],0),
      Shift(331,339,0),
      False
    ),
    #has have exceeded the max hours work on third of four weeks
    (
      Vigilant(0,0,[],[],[],0,[0,44,44,0],0),
      Shift(332,340,0),
      False
    )
  ])
def test_should_check_if_vigilant_is_available_correctly(vigilant:Vigilant, shift: Shift, expected: bool):
    assert vigilantService.has_enough_hours_to_work_in_week(vigilant,shift) == expected

@pytest.mark.parametrize("vigilant, shift, expected",[
    #No shift case
    (
      Vigilant(0,0,[],{},[],0,[0,0],0),
      Shift(6,13,0),
      True
    ),
    #Assingin shift in existing same shift
    (
      Vigilant(0,0,[],[
        Shift_place(Shift(6,13,0),1)
      ],[],0,[8,0],0),
      Shift(6,13,0),
      False
    ),
    #Doesn has enough time rest to take new shift case initial shift
    (
      Vigilant(0,0,[],[
        Shift_place(Shift(0,5,0),1)
      ],[],0,[8,0],0),
      Shift(6,13,0),
      False
    )
    #Doesn has enough time rest to take new shift case before new shift
    ,(
      Vigilant(0,0,[],[Shift_place(Shift(152,159,0),1)],[],0,[8],0),
      Shift(160,167,0),
      False
    ),
    #Doesn has enough time rest to take new shift case after new shift
    (
      Vigilant(0,0,[],[Shift_place(Shift(152,159,0),1)],[],0,[8],0),
      Shift(140,151,0),
      False
    )
])
def test_should_vigilant_has_enough_time_to_rest_with_new_shifts(vigilant:Vigilant, shift: Shift, expected: bool):
  assert vigilantService.is_available_on_shift(vigilant,shift) == expected

@pytest.mark.parametrize("vigilant, shift, expected",[
    #has enought rest time after but not before new shift
    (
      Vigilant(0,0,[],[Shift_place(Shift(100,114,0),1),Shift_place(Shift(154,167,0),1)],[],0,[8],0),
      Shift(130,137,0),
      False
    ),
    #has enought rest time before but not after new shift
    (
      Vigilant(0,0,[],[Shift_place(Shift(100,113,0),1),Shift_place(Shift(153,167,0),1)],[],0,[8],0),
      Shift(130,137,0),
      False
    ),
    #has enought rest time before and after new shift
    (
      Vigilant(0,0,[],[Shift_place(Shift(100,113,0),1),Shift_place(Shift(154,165,0),1)],[],0,[8],0),
      Shift(130,137,0),
      True
    ),
    #has enought rest time before and after new shift
    (
      Vigilant(0,0,[],[Shift_place(Shift(0,7,0),1),Shift_place(Shift(48,55,0),1)],[],0,[8],0),
      Shift(24,31,0),
      True
    )
])
def test_should_vigilant_has_enough_time_to_rest_between_shifts(vigilant:Vigilant, shift: Shift, expected: bool):
  assert vigilantService.is_available_on_shift(vigilant,shift) == expected

@pytest.mark.parametrize("site_id, vigilantes, expected",[
    (
      1,
      [
        Vigilant(1,1,[],{},[],0,[],0),
        Vigilant(2,1,[],{},[],0,[],0),
        Vigilant(3,0,[],{},[],0,[],0),
        Vigilant(4,2,[],{},[],0,[],0),
        Vigilant(5,2,[],{},[],0,[],0),
        Vigilant(6,1,[],{},[],0,[],0),
        Vigilant(7,1,[],{},[],0,[],0),
        Vigilant(8,0,[],{},[],0,[],0),
        Vigilant(9,1,[],{},[],0,[],0),
      ],
      [
        Vigilant(1,1,[],{},[],0,[],0),
        Vigilant(2,1,[],{},[],0,[],0),
        Vigilant(6,1,[],{},[],0,[],0),
        Vigilant(7,1,[],{},[],0,[],0),
        Vigilant(9,1,[],{},[],0,[],0)
      ]      
    )
])
def test_should_obtain_vigilantes_correctly_on_default_place(site_id: int, vigilantes: List[Vigilant], expected: List[Vigilant]):  
  VigilantAssigment.expected_places_to_look_out_by_vigilants = {1:[1,2,6,7,9],2:[4,5]} 
  assert vigilantService.obtain_vigilants_in_default_for_site(site_id,vigilantes) == expected

# @pytest.mark.parametrize("site_id, vigilantes, expected",[
#     (
#       1,
#       [
#         Vigilant(1,1,[],{},[],0,[],0),
#         Vigilant(2,1,[],{},[],0,[],0),
#         Vigilant(3,0,[],{},[],0,[],0),
#         Vigilant(4,2,[],{},[],0,[],0),
#         Vigilant(5,2,[],{},[],0,[],0),
#         Vigilant(6,1,[],{},[],0,[],0),
#         Vigilant(7,1,[],{},[],0,[],0),
#         Vigilant(8,0,[],{},[],0,[],0),
#         Vigilant(9,1,[],{},[],0,[],0),
#       ],
#       [
#         Vigilant(1,1,[],{},[],0,[],0),
#         Vigilant(2,1,[],{},[],0,[],0),
#         Vigilant(6,1,[],{},[],0,[],0),
#         Vigilant(7,1,[],{},[],0,[],0),
#         Vigilant(9,1,[],{},[],0,[],0)
#       ]      
#     )
# ])
# def test_should_get_order_vigilantes_index_in_place_by_distance(site_id: int, vigilantes: List[Vigilant], expected: List[Vigilant]):  
#   assert vigilantService.get_order_vigilantes_index_in_place_by_distance(site_id,vigilantes) == expected
