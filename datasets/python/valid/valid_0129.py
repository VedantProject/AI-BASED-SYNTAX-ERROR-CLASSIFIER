def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([73, 30, 18, 62, 94])
print(f"min={lo}, max={hi}")
