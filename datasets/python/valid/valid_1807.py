def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([44, 51, 64, 75, 46])
print(f"min={lo}, max={hi}")
