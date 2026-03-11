def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([50, 17, 96, 16, 91])
print(f"min={lo}, max={hi}")
