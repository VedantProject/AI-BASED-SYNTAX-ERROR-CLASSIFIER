def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([19, 81, 90, 51, 38])
print(f"min={lo}, max={hi}")
