import pytest
from utils.order import Order


@pytest.mark.parametrize("list,num_return,persentage",[
    (
        [1,2,3,4,5,6,7,8,9,10],
        1,
        1
    ),
    (
        [1,2],
        1,
        0.1
    ),
    (
        [1,2,3,4,5,6,7,8,9,10,11,2,13,14],
        2,
        0.5
    ),
    (
        [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20],
        3,
        0.5
    ),
     (
        [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20],
        10,
        0.5
    )
])
def test_list_restrited(list, num_return, persentage):
    response = Order.list_restricted(list, num_return, persentage )
    print(f"\n{response} esta dentro de {list} con porsentaje de {persentage}")
    for number in response:
        if number in [1,2,3,4,5,6,7,8,9,10]:
            assert True
        else:
            assert False


