def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([12, 37, 85, 38, 56])
print(f"min={lo}, max={hi}")
