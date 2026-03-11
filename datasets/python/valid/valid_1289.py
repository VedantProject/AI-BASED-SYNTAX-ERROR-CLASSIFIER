def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([2, 49, 67, 17, 94])
print(f"min={lo}, max={hi}")
