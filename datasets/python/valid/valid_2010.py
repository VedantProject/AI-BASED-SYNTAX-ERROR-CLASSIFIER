def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([52, 64, 17, 80, 85])
print(f"min={lo}, max={hi}")
