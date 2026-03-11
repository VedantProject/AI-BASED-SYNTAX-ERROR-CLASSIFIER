def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([71, 99, 38, 34, 60])
print(f"min={lo}, max={hi}")
