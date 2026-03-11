def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([62, 25, 11, 31, 45])
print(f"min={lo}, max={hi}")
