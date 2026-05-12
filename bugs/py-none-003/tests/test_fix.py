import pytest
from buggy import safe_first


def test_non_empty():
    assert safe_first([1, 2, 3]) == 1


def test_empty():
    assert safe_first([]) is None


def test_single():
    assert safe_first([42]) == 42


def test_strings():
    assert safe_first(["a", "b"]) == "a"
