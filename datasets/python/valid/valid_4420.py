def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([84, 91, 35, 11, 2])
print(f"min={lo}, max={hi}")
