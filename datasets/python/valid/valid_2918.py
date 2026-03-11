def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([28, 13, 62, 72, 21])
print(f"min={lo}, max={hi}")
