def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([77, 64, 63, 55])
print(f"min={lo}, max={hi}")
