def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([97, 64, 32, 24, 55])
print(f"min={lo}, max={hi}")
