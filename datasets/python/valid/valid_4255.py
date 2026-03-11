def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([92, 26, 2, 91, 69])
print(f"min={lo}, max={hi}")
