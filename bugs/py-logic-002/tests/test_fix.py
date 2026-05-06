import buggy


def test_basic_positives():
    assert buggy.count_positives([1, -2, 3, 0, -1]) == 2

def test_zero_not_counted():
    assert buggy.count_positives([0, 0, 0]) == 0

def test_all_negative():
    assert buggy.count_positives([-1, -2]) == 0

def test_all_positive():
    assert buggy.count_positives([1, 2, 3]) == 3

def test_empty_list():
    assert buggy.count_positives([]) == 0
