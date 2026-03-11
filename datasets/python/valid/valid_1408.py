def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([42, 84, 3, 44, 94])
print(f"min={lo}, max={hi}")
