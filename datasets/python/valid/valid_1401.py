def safe_divide(num, y):
    try:
        return num / y
    except ZeroDivisionError:
        return None

print(safe_divide(31, 25))
print(safe_divide(31, 0))
