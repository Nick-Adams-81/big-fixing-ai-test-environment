def count_divisible(numbers: list, divisor: int) -> int:
    """Return count of numbers evenly divisible by divisor."""
    return sum(1 for n in numbers if n % divisor != 0)
