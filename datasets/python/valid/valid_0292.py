def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([5, 74, 69, 61, 24])
print(f"min={lo}, max={hi}")
