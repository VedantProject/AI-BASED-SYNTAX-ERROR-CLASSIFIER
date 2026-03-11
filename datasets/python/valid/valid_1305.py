def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([18, 96, 73, 73, 95])
print(f"min={lo}, max={hi}")
