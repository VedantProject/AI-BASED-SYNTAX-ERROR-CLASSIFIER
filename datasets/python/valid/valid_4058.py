def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([38, 13, 37, 90, 60])
print(f"min={lo}, max={hi}")
