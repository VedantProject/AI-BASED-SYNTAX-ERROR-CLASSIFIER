def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([95, 80, 23, 63, 20])
print(f"min={lo}, max={hi}")
