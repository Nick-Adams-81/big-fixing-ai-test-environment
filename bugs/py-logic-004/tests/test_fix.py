import buggy


def test_basic_max():
    assert buggy.find_max([3, 1, 4, 1, 5, 9, 2, 6]) == 9

def test_all_negative():
    assert buggy.find_max([-1, -5, -3]) == -1

def test_single_element():
    assert buggy.find_max([42]) == 42

def test_already_sorted():
    assert buggy.find_max([1, 2, 3, 4, 5]) == 5

def test_reverse_sorted():
    assert buggy.find_max([5, 4, 3, 2, 1]) == 5
