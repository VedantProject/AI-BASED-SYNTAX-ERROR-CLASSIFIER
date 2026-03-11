def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([78, 76, 59, 71, 45])
print(f"min={lo}, max={hi}")
