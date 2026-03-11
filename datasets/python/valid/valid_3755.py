def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([98, 81, 88, 20, 60])
print(f"min={lo}, max={hi}")
