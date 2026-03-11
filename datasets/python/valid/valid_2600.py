def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([36, 77, 1, 35, 75])
print(f"min={lo}, max={hi}")
