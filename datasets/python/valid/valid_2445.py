def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([69, 91, 6, 20, 67])
print(f"min={lo}, max={hi}")
