def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([62, 98, 18, 88, 64])
print(f"min={lo}, max={hi}")
