def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([1, 61, 68, 62, 76])
print(f"min={lo}, max={hi}")
