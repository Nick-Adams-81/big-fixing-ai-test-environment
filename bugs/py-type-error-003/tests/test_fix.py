import pytest
from buggy import is_positive


def test_positive():
    assert is_positive(5) is True


def test_negative():
    assert is_positive(-3) is False


def test_zero():
    assert is_positive(0) is False


def test_float():
    assert is_positive(0.1) is True


def test_large():
    assert is_positive(1000) is True
