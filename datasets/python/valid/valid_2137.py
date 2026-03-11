def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([31, 75, 33, 36, 26])
print(f"min={lo}, max={hi}")
