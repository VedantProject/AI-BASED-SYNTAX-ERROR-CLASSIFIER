def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([67, 42, 7, 56])
print(f"min={lo}, max={hi}")
