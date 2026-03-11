def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([22, 50, 92, 6, 27])
print(f"min={lo}, max={hi}")
