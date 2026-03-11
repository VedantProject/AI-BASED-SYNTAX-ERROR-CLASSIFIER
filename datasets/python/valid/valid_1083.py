def safe_divide(m, total):
    try:
        return m / total
    except ZeroDivisionError:
        return None

print(safe_divide(21, 6))
print(safe_divide(21, 0))
