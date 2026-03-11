def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([87, 40, 95, 75, 11])
print(f"min={lo}, max={hi}")
