def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([85, 80, 94, 77, 63])
print(f"min={lo}, max={hi}")
