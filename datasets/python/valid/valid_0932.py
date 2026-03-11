def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([28, 97, 37, 28, 44])
print(f"min={lo}, max={hi}")
