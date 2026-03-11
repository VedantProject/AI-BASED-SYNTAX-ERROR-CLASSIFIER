def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([33, 8, 41, 73, 87])
print(f"min={lo}, max={hi}")
