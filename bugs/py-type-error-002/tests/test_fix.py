import pytest
from buggy import total_length


def test_basic():
    assert total_length(["hello", "world"]) == 10


def test_single():
    assert total_length(["abc"]) == 3


def test_empty_list():
    assert total_length([]) == 0


def test_empty_strings():
    assert total_length(["", "", ""]) == 0


def test_mixed():
    assert total_length(["a", "bb", "ccc"]) == 6
