def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([48, 41, 49, 61, 36])
print(f"min={lo}, max={hi}")
