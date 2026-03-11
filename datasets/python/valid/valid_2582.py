def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([33, 87, 41, 70, 99])
print(f"min={lo}, max={hi}")
