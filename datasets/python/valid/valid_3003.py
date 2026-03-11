def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([19, 2, 13, 98])
print(f"min={lo}, max={hi}")
