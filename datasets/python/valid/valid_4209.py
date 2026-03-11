def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([95, 4, 66, 84, 46])
print(f"min={lo}, max={hi}")
