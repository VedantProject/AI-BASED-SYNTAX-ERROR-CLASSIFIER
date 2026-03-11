def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([22, 42, 82, 3, 17])
print(f"min={lo}, max={hi}")
