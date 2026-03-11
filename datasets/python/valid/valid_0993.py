def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([39, 5, 5, 6, 30])
print(f"min={lo}, max={hi}")
