def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([42, 45, 20, 54, 33])
print(f"min={lo}, max={hi}")
