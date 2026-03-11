def safe_divide(size, y):
    try:
        return size / y
    except ZeroDivisionError:
        return None

print(safe_divide(42, 33))
print(safe_divide(42, 0))
