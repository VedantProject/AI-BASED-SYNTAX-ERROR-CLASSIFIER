def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([46, 49, 70, 64, 15])
print(f"min={lo}, max={hi}")
