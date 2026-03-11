def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([41, 14, 69, 45, 9])
print(f"min={lo}, max={hi}")
