def safe_divide(item, b):
    try:
        return item / b
    except ZeroDivisionError:
        return None

print(safe_divide(17, 42))
print(safe_divide(17, 0))
