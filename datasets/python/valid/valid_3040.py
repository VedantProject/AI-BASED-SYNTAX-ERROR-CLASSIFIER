def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([38, 2, 84, 83, 77])
print(f"min={lo}, max={hi}")
