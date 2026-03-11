def safe_divide(m, count):
    try:
        return m / count
    except ZeroDivisionError:
        return None

print(safe_divide(19, 24))
print(safe_divide(19, 0))
