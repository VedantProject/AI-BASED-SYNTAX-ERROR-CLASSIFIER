def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([23, 43, 91, 39])
print(f"min={lo}, max={hi}")
