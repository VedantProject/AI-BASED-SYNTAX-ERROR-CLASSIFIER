def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([22, 81, 15, 2, 93])
print(f"min={lo}, max={hi}")
