def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([29, 64, 47, 41, 28])
print(f"min={lo}, max={hi}")
