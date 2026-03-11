def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([63, 66, 31, 4, 72])
print(f"min={lo}, max={hi}")
