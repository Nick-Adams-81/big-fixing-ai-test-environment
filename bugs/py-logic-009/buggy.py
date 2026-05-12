def rotate_right(lst: list, k: int) -> list:
    """Rotate list right by k positions."""
    if not lst:
        return lst
    k = k % len(lst)
    return lst[k:] + lst[:k]
