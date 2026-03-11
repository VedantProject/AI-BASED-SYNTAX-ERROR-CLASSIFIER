def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([11, 66, 24, 73, 37])
print(f"min={lo}, max={hi}")
