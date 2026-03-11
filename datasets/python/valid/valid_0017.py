def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([96, 54, 33, 65])
print(f"min={lo}, max={hi}")
