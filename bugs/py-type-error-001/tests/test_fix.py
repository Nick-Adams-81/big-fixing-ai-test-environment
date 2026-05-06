import buggy


def test_average_with_remainder():
    assert buggy.average([1, 2, 3, 4]) == 2.5

def test_average_whole_number():
    assert buggy.average([10, 20]) == 15.0

def test_single_element():
    assert buggy.average([7]) == 7.0

def test_average_returns_float():
    result = buggy.average([1, 2])
    assert isinstance(result, float)
