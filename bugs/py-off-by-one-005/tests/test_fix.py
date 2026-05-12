from buggy import repeat_str


def test_repeat_three():
    assert repeat_str("ab", 3) == "ababab"


def test_repeat_once():
    assert repeat_str("hi", 1) == "hi"


def test_repeat_zero():
    assert repeat_str("x", 0) == ""


def test_repeat_five():
    assert repeat_str("a", 5) == "aaaaa"


def test_repeat_empty():
    assert repeat_str("", 4) == ""
