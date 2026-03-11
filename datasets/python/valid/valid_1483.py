def safe_divide(size, b):
    try:
        return size / b
    except ZeroDivisionError:
        return None

print(safe_divide(38, 7))
print(safe_divide(38, 0))
