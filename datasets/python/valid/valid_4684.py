def safe_divide(z, y):
    try:
        return z / y
    except ZeroDivisionError:
        return None

print(safe_divide(16, 12))
print(safe_divide(16, 0))
