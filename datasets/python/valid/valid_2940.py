def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([95, 10, 52, 52, 95])
print(f"min={lo}, max={hi}")
