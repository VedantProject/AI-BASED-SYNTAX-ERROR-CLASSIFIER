def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([45, 90, 44, 12, 35])
print(f"min={lo}, max={hi}")
