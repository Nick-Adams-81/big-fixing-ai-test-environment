from buggy import first_n


def test_first_three():
    assert first_n([1, 2, 3, 4, 5], 3) == [1, 2, 3]


def test_first_one():
    assert first_n([10, 20, 30], 1) == [10]


def test_first_all():
    lst = [1, 2, 3]
    assert first_n(lst, 3) == lst


def test_first_two():
    assert first_n(list(range(10)), 2) == [0, 1]


def test_zero():
    assert first_n([1, 2, 3], 0) == []
