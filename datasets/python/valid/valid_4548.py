def safe_divide(res, y):
    try:
        return res / y
    except ZeroDivisionError:
        return None

print(safe_divide(50, 38))
print(safe_divide(50, 0))
