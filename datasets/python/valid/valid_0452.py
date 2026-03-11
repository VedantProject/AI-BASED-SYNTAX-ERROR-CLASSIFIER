def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([8, 75, 64, 17, 36])
print(f"min={lo}, max={hi}")
