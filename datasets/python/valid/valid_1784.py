def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([32, 87, 3, 36, 59])
print(f"min={lo}, max={hi}")
