def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([24, 62, 59, 48, 99])
print(f"min={lo}, max={hi}")
