def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([14, 75, 38, 64, 68])
print(f"min={lo}, max={hi}")
