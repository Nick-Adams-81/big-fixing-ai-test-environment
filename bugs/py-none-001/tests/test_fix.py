import buggy


def test_normal_string():
    assert buggy.get_name_length("hello") == 5

def test_none_returns_zero():
    assert buggy.get_name_length(None) == 0

def test_empty_string():
    assert buggy.get_name_length("") == 0

def test_longer_string():
    assert buggy.get_name_length("Claude") == 6
