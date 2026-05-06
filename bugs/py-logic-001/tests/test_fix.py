import buggy


def test_even_number():
    assert buggy.is_even(4) is True

def test_odd_number():
    assert buggy.is_even(3) is False

def test_zero_is_even():
    assert buggy.is_even(0) is True

def test_negative_even():
    assert buggy.is_even(-2) is True

def test_negative_odd():
    assert buggy.is_even(-3) is False
