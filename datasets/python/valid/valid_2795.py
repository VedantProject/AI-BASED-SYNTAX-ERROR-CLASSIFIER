def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([46, 48, 13, 8, 20])
print(f"min={lo}, max={hi}")
