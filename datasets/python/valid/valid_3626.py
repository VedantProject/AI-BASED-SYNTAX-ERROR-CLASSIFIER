def safe_divide(prod, n):
    try:
        return prod / n
    except ZeroDivisionError:
        return None

print(safe_divide(26, 15))
print(safe_divide(26, 0))
