def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([31, 67, 47, 45, 77])
print(f"min={lo}, max={hi}")
