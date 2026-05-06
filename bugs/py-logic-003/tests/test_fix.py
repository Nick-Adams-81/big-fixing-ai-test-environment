import pytest
import buggy


def test_freezing_point():
    assert buggy.celsius_to_fahrenheit(0) == 32.0

def test_boiling_point():
    assert buggy.celsius_to_fahrenheit(100) == 212.0

def test_body_temperature():
    assert buggy.celsius_to_fahrenheit(37) == pytest.approx(98.6, rel=1e-3)

def test_negative_forty_equal():
    assert buggy.celsius_to_fahrenheit(-40) == -40.0
