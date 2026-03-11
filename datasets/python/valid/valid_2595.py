def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([38, 55, 69, 4])
print(f"min={lo}, max={hi}")
