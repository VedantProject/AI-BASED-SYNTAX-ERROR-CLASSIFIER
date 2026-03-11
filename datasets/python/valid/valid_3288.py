def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([20, 7, 10, 64, 4])
print(f"min={lo}, max={hi}")
