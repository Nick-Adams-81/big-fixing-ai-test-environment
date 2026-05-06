def sum_except_first(numbers):
    """Return the sum of all elements except the first."""
    total = 0
    for i in range(len(numbers)):
        total += numbers[i]
    return total
