def safe_divide(m, total):
    try:
        return m / total
    except ZeroDivisionError:
        return None

print(safe_divide(11, 23))
print(safe_divide(11, 0))
