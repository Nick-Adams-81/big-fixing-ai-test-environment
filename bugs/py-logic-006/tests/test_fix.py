from buggy import clamp


def test_in_range():
    assert clamp(5.0, 0.0, 10.0) == 5.0


def test_at_lo():
    assert clamp(0.0, 0.0, 10.0) == 0.0


def test_at_hi():
    assert clamp(10.0, 0.0, 10.0) == 10.0


def test_below_lo():
    assert clamp(-1.0, 0.0, 10.0) == 0.0


def test_above_hi():
    assert clamp(11.0, 0.0, 10.0) == 10.0
