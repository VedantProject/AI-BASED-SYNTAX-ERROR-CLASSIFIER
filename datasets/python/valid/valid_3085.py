def safe_divide(x, z):
    try:
        return x / z
    except ZeroDivisionError:
        return None

print(safe_divide(6, 42))
print(safe_divide(6, 0))
