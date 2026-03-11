def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([6, 72, 75, 20, 81])
print(f"min={lo}, max={hi}")
