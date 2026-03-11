def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([57, 20, 70, 93, 97])
print(f"min={lo}, max={hi}")
