def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([9, 26, 25, 60, 14])
print(f"min={lo}, max={hi}")
