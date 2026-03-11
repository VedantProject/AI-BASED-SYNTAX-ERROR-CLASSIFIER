def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([61, 9, 73, 65, 7])
print(f"min={lo}, max={hi}")
