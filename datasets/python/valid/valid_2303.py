def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([16, 32, 80, 5, 83])
print(f"min={lo}, max={hi}")
