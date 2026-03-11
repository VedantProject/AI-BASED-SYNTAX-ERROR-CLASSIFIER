def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([54, 35, 80, 62, 92])
print(f"min={lo}, max={hi}")
