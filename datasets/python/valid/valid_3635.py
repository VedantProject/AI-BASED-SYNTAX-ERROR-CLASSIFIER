def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([2, 27, 19, 40, 3])
print(f"min={lo}, max={hi}")
