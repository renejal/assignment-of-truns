import pytest
from utils import aleatory

@pytest.mark.parametrize("start, end, list",
[
(2,5,[3]),
(2,5,[3,4]),
(2,5,[3,5,4]),
(2,5,[3]),
(2,5,[3,2,3,4,5])
])
def test_aleatory_no_list(start, end, list):
    for i in range(20):
        number = aleatory.get_random_int(start, end, list)
        assert number != 3

    
