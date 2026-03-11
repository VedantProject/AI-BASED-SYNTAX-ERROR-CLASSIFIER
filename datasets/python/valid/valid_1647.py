def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([56, 19, 21, 30, 77])
print(f"min={lo}, max={hi}")
