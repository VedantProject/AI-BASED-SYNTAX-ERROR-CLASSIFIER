def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([29, 30, 95, 83, 32])
print(f"min={lo}, max={hi}")
