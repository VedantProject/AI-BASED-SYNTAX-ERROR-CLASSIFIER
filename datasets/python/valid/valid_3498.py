def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([49, 77, 45, 45, 19])
print(f"min={lo}, max={hi}")
