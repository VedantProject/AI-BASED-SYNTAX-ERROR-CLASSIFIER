def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([72, 58, 49, 94, 10])
print(f"min={lo}, max={hi}")
