def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([51, 65, 79, 42, 67])
print(f"min={lo}, max={hi}")
