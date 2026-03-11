def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([23, 8, 55, 99, 11])
print(f"min={lo}, max={hi}")
