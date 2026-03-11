def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([34, 19, 1, 55, 83])
print(f"min={lo}, max={hi}")
