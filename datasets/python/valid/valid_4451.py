def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([34, 77, 78, 84, 35])
print(f"min={lo}, max={hi}")
