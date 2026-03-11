def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([13, 33, 32, 16, 20])
print(f"min={lo}, max={hi}")
