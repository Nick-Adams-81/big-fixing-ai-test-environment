import buggy


def test_excludes_first_element():
    assert buggy.sum_except_first([10, 1, 2, 3]) == 6

def test_single_element_returns_zero():
    assert buggy.sum_except_first([5]) == 0

def test_two_elements_returns_second():
    assert buggy.sum_except_first([100, 42]) == 42

def test_empty_list_returns_zero():
    assert buggy.sum_except_first([]) == 0
