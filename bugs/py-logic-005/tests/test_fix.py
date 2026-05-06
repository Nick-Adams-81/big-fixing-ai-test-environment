import buggy


def test_palindrome_odd_length():
    assert buggy.is_palindrome("racecar") is True

def test_not_palindrome():
    assert buggy.is_palindrome("hello") is False

def test_single_character():
    assert buggy.is_palindrome("a") is True

def test_empty_string():
    assert buggy.is_palindrome("") is True

def test_palindrome_even_length():
    assert buggy.is_palindrome("abba") is True
