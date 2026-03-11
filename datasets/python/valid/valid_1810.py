def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([31, 97, 84, 94, 27])
print(f"min={lo}, max={hi}")
