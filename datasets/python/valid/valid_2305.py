def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([52, 83, 76, 1, 89])
print(f"min={lo}, max={hi}")
