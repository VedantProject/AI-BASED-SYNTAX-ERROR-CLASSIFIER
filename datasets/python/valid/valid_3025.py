def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([62, 11, 69, 30])
print(f"min={lo}, max={hi}")
