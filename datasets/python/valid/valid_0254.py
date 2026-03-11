def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([58, 3, 9, 28, 32])
print(f"min={lo}, max={hi}")
