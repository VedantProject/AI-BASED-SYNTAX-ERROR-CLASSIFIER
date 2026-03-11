def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([64, 64, 54, 57, 78])
print(f"min={lo}, max={hi}")
