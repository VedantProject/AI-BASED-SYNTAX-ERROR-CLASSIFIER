def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([21, 57, 62, 18, 79])
print(f"min={lo}, max={hi}")
