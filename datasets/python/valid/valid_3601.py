def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([81, 13, 90, 3])
print(f"min={lo}, max={hi}")
