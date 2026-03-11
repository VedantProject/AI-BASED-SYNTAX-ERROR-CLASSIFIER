def safe_divide(temp, y):
    try:
        return temp / y
    except ZeroDivisionError:
        return None

print(safe_divide(31, 42))
print(safe_divide(31, 0))
