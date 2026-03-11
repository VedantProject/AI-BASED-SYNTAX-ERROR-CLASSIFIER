def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([93, 88, 95, 66, 53])
print(f"min={lo}, max={hi}")
