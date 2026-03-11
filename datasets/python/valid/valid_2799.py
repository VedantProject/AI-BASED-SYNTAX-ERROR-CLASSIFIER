def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([50, 72, 6, 84, 48])
print(f"min={lo}, max={hi}")
