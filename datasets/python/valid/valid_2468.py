def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([33, 28, 62, 65, 45])
print(f"min={lo}, max={hi}")
