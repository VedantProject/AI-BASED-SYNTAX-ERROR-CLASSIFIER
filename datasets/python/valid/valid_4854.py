def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([33, 54, 45, 66])
print(f"min={lo}, max={hi}")
