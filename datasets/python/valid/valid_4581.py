def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([35, 58, 24, 32, 14])
print(f"min={lo}, max={hi}")
