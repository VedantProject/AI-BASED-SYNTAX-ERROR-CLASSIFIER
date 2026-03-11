def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([9, 93, 40, 68, 5])
print(f"min={lo}, max={hi}")
