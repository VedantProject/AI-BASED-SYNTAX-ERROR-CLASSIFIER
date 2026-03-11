def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([32, 95, 13, 62, 10])
print(f"min={lo}, max={hi}")
