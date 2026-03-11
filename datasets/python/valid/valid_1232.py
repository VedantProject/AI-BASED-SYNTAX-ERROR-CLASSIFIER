def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([80, 82, 38, 76])
print(f"min={lo}, max={hi}")
