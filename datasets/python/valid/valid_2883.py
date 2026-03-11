def safe_divide(val, z):
    try:
        return val / z
    except ZeroDivisionError:
        return None

print(safe_divide(15, 13))
print(safe_divide(15, 0))
