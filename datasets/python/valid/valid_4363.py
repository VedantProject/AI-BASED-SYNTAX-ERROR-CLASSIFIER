def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([61, 48, 66, 20, 82])
print(f"min={lo}, max={hi}")
