def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([42, 23, 96, 97, 55])
print(f"min={lo}, max={hi}")
