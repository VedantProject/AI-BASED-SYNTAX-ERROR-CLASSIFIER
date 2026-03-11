def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([12, 36, 57, 81, 12])
print(f"min={lo}, max={hi}")
