def repeat_str(s: str, n: int) -> str:
    """Return string s repeated n times."""
    result = ""
    for _ in range(n - 1):
        result += s
    return result
