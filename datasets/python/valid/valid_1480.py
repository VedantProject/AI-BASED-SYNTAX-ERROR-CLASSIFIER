def safe_divide(a, count):
    try:
        return a / count
    except ZeroDivisionError:
        return None

print(safe_divide(21, 35))
print(safe_divide(21, 0))
