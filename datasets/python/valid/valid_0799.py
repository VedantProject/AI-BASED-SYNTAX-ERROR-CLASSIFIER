def safe_divide(m, item):
    try:
        return m / item
    except ZeroDivisionError:
        return None

print(safe_divide(25, 31))
print(safe_divide(25, 0))
