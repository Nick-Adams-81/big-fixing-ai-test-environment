from buggy import rotate_right


def test_rotate_by_1():
    assert rotate_right([1, 2, 3, 4, 5], 1) == [5, 1, 2, 3, 4]


def test_rotate_by_2():
    assert rotate_right([1, 2, 3, 4, 5], 2) == [4, 5, 1, 2, 3]


def test_rotate_by_0():
    assert rotate_right([1, 2, 3], 0) == [1, 2, 3]


def test_empty():
    assert rotate_right([], 3) == []


def test_full_rotation():
    lst = [1, 2, 3]
    assert rotate_right(lst, 3) == lst
