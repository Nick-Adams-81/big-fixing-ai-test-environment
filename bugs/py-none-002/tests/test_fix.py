import pytest
from buggy import get_value


def test_existing_key():
    assert get_value({"name": "  Alice  "}, "name") == "Alice"


def test_missing_key():
    assert get_value({}, "name") == ""


def test_no_whitespace():
    assert get_value({"x": "hello"}, "x") == "hello"


def test_whitespace_only():
    assert get_value({"x": "   "}, "x") == ""
