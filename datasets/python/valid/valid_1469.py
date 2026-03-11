def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([65, 16, 83, 86, 70])
print(f"min={lo}, max={hi}")
