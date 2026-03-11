def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([11, 31, 67, 35, 71])
print(f"min={lo}, max={hi}")
