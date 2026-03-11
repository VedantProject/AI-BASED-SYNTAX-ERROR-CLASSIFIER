def safe_divide(x, y):
    try:
        return x / y
    except ZeroDivisionError:
        return None

print(safe_divide(31, 49))
print(safe_divide(31, 0))
