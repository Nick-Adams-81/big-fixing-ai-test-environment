from buggy import max_subarray_sum


def test_all_positive():
    assert max_subarray_sum([1, 2, 3, 4]) == 10


def test_mixed():
    assert max_subarray_sum([-2, 1, -3, 4, -1, 2, 1, -5, 4]) == 6


def test_all_negative():
    assert max_subarray_sum([-3, -1, -2]) == -1


def test_single():
    assert max_subarray_sum([5]) == 5


def test_reset():
    assert max_subarray_sum([3, -10, 4]) == 4
