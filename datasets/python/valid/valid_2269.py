def safe_divide(prod, size):
    try:
        return prod / size
    except ZeroDivisionError:
        return None

print(safe_divide(24, 32))
print(safe_divide(24, 0))
