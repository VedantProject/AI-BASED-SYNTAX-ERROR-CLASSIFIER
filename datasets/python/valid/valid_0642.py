def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([6, 69, 82, 55, 13])
print(f"min={lo}, max={hi}")
