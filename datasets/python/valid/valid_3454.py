def safe_divide(prod, z):
    try:
        return prod / z
    except ZeroDivisionError:
        return None

print(safe_divide(7, 2))
print(safe_divide(7, 0))
