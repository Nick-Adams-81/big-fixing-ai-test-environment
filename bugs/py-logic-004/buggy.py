def find_max(numbers):
    """Return the maximum value in a non-empty list."""
    max_val = numbers[0]
    for n in numbers[1:]:
        if n < max_val:
            max_val = n
    return max_val
