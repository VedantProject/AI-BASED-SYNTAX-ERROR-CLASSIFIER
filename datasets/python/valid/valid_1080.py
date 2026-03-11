def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([39, 69, 69, 47, 36])
print(f"min={lo}, max={hi}")
