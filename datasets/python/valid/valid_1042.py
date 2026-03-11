def safe_divide(val, b):
    try:
        return val / b
    except ZeroDivisionError:
        return None

print(safe_divide(50, 12))
print(safe_divide(50, 0))
