def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([67, 41, 42, 51, 7])
print(f"min={lo}, max={hi}")
