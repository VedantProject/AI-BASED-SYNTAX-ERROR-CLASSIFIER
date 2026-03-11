def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([58, 86, 54, 80, 77])
print(f"min={lo}, max={hi}")
