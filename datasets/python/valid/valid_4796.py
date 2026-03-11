def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([11, 37, 95, 74, 84])
print(f"min={lo}, max={hi}")
