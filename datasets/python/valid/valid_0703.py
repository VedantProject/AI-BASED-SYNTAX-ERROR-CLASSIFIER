def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([52, 21, 33, 33, 19])
print(f"min={lo}, max={hi}")
