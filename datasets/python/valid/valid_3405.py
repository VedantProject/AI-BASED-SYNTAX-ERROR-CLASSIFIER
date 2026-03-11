def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([64, 21, 46, 89, 17])
print(f"min={lo}, max={hi}")
