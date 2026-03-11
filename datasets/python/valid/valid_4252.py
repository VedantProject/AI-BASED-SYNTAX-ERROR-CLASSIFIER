def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([56, 21, 70, 83, 15])
print(f"min={lo}, max={hi}")
