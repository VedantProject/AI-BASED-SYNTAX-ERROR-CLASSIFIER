def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([51, 49, 93, 81, 19])
print(f"min={lo}, max={hi}")
