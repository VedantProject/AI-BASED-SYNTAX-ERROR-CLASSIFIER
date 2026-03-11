def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([41, 35, 98, 96, 21])
print(f"min={lo}, max={hi}")
