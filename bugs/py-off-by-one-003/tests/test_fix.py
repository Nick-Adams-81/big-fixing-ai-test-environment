import buggy


def test_finds_middle_element():
    assert buggy.binary_search([1, 3, 5, 7, 9], 5) == 2

def test_finds_first_element():
    assert buggy.binary_search([1, 3, 5, 7, 9], 1) == 0

def test_finds_last_element():
    assert buggy.binary_search([1, 3, 5, 7, 9], 9) == 4

def test_not_found_returns_negative_one():
    assert buggy.binary_search([1, 3, 5, 7, 9], 10) == -1

def test_not_found_smaller_than_all():
    assert buggy.binary_search([1, 3, 5, 7, 9], 0) == -1
