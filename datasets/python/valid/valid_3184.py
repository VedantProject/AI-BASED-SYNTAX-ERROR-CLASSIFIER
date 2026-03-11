def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([75, 98, 89, 27, 15])
print(f"min={lo}, max={hi}")
