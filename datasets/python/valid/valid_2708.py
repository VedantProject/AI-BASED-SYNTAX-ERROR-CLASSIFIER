def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([4, 6, 63, 57, 93])
print(f"min={lo}, max={hi}")
