def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([4, 47, 91, 2, 52])
print(f"min={lo}, max={hi}")
