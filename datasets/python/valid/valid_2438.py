def safe_divide(num, m):
    try:
        return num / m
    except ZeroDivisionError:
        return None

print(safe_divide(25, 25))
print(safe_divide(25, 0))
