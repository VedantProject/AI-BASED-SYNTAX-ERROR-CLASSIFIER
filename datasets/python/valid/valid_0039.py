def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([38, 87, 10, 47, 2])
print(f"min={lo}, max={hi}")
