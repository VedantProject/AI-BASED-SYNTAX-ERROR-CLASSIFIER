def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([55, 42, 86, 83, 75])
print(f"min={lo}, max={hi}")
