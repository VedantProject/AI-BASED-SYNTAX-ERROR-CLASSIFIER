def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([31, 11, 9, 46, 37])
print(f"min={lo}, max={hi}")
