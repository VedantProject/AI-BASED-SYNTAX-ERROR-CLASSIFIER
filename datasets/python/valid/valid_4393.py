def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([87, 21, 50, 98])
print(f"min={lo}, max={hi}")
