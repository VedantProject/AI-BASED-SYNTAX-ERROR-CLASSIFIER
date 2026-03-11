def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([5, 50, 43, 83])
print(f"min={lo}, max={hi}")
