def safe_divide(m, count):
    try:
        return m / count
    except ZeroDivisionError:
        return None

print(safe_divide(35, 16))
print(safe_divide(35, 0))
