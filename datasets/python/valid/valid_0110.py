def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([66, 11, 20, 57, 81])
print(f"min={lo}, max={hi}")
