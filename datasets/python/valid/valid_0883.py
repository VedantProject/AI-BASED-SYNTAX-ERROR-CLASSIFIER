def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([7, 35, 31, 73, 9])
print(f"min={lo}, max={hi}")
