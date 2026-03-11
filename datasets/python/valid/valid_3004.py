def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([89, 73, 16, 86, 44])
print(f"min={lo}, max={hi}")
