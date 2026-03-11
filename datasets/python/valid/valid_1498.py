def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([15, 6, 46, 96, 33])
print(f"min={lo}, max={hi}")
