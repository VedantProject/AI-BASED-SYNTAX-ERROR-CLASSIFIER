def safe_divide(a, m):
    try:
        return a / m
    except ZeroDivisionError:
        return None

print(safe_divide(23, 35))
print(safe_divide(23, 0))
