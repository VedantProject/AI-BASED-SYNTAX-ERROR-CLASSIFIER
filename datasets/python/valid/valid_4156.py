def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([68, 35, 99, 65, 13])
print(f"min={lo}, max={hi}")
