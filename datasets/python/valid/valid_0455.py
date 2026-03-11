def safe_divide(x, item):
    try:
        return x / item
    except ZeroDivisionError:
        return None

print(safe_divide(42, 26))
print(safe_divide(42, 0))
