def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([10, 69, 27, 8, 76])
print(f"min={lo}, max={hi}")
