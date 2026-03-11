def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([63, 24, 36, 56, 41])
print(f"min={lo}, max={hi}")
