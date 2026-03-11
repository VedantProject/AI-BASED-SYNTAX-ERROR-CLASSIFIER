def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([63, 60, 7, 94, 8])
print(f"min={lo}, max={hi}")
