def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([28, 25, 64, 16])
print(f"min={lo}, max={hi}")
