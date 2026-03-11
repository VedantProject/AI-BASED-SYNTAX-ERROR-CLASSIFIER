def safe_divide(a, m):
    try:
        return a / m
    except ZeroDivisionError:
        return None

print(safe_divide(35, 21))
print(safe_divide(35, 0))
