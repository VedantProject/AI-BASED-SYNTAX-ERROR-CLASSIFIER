def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([78, 50, 50, 45, 18])
print(f"min={lo}, max={hi}")
