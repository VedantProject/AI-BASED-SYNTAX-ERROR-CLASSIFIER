def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([14, 43, 53, 31, 34])
print(f"min={lo}, max={hi}")
