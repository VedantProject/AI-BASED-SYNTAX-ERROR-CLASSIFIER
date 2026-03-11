def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([36, 99, 32, 53, 60])
print(f"min={lo}, max={hi}")
