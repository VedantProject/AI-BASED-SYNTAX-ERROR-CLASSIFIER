def safe_divide(m, num):
    try:
        return m / num
    except ZeroDivisionError:
        return None

print(safe_divide(21, 24))
print(safe_divide(21, 0))
