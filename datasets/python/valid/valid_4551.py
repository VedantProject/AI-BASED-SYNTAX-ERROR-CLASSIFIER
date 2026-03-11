def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([14, 36, 87, 47, 40])
print(f"min={lo}, max={hi}")
