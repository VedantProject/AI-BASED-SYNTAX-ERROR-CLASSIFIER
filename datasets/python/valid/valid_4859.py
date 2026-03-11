def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([4, 96, 83, 45, 86])
print(f"min={lo}, max={hi}")
