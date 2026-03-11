def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([58, 22, 85, 74, 52])
print(f"min={lo}, max={hi}")
