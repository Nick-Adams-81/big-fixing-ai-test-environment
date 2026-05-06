import buggy


def test_returns_correct_count():
    assert buggy.first_n([1, 2, 3, 4, 5], 3) == [1, 2, 3]

def test_returns_all_when_n_equals_length():
    assert buggy.first_n([1, 2], 2) == [1, 2]

def test_returns_one_element():
    assert buggy.first_n([1, 2, 3], 1) == [1]

def test_returns_empty_when_n_is_zero():
    assert buggy.first_n([1, 2, 3], 0) == []
