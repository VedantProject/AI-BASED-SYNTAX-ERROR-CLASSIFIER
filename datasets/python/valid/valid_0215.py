def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([34, 82, 16, 65])
print(f"min={lo}, max={hi}")
