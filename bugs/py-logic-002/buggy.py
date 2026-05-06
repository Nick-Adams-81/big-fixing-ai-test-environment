def count_positives(numbers):
    """Return the count of positive numbers (> 0) in the list."""
    count = 0
    for n in numbers:
        if n >= 0:
            count += 1
    return count
