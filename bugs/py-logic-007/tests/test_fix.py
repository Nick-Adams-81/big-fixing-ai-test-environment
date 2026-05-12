from buggy import count_divisible


def test_divisible_by_2():
    assert count_divisible([1, 2, 3, 4, 6], 2) == 3


def test_divisible_by_3():
    assert count_divisible([3, 6, 9, 10], 3) == 3


def test_none_divisible():
    assert count_divisible([1, 2, 4], 3) == 0


def test_all_divisible():
    assert count_divisible([4, 8, 12], 4) == 3


def test_empty():
    assert count_divisible([], 5) == 0
