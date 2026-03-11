def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([86, 11, 76, 75])
print(f"min={lo}, max={hi}")
