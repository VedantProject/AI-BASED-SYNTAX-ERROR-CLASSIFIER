def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([56, 74, 24, 75, 66])
print(f"min={lo}, max={hi}")
