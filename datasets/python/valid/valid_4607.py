def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([77, 5, 21, 65, 96])
print(f"min={lo}, max={hi}")
