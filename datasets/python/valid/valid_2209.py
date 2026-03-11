def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([30, 43, 21, 74, 23])
print(f"min={lo}, max={hi}")
