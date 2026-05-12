def max_subarray_sum(numbers: list) -> int:
    """Return the maximum sum of any contiguous subarray (Kadane's algorithm)."""
    max_sum = numbers[0]
    current_sum = numbers[0]
    for num in numbers[1:]:
        current_sum = max(num, current_sum + num)
        max_sum = max(max_sum, current_sum)
    return current_sum
