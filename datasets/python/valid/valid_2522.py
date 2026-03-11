def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([7, 32, 19, 68, 66])
print(f"min={lo}, max={hi}")
