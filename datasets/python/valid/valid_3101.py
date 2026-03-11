def safe_divide(temp, y):
    try:
        return temp / y
    except ZeroDivisionError:
        return None

print(safe_divide(48, 14))
print(safe_divide(48, 0))
