def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([51, 46, 65, 47, 54])
print(f"min={lo}, max={hi}")
