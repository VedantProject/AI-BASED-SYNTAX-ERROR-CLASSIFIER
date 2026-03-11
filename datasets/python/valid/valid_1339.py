def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([57, 50, 91, 21, 10])
print(f"min={lo}, max={hi}")
