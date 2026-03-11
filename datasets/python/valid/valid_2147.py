def safe_divide(n, data):
    try:
        return n / data
    except ZeroDivisionError:
        return None

print(safe_divide(30, 24))
print(safe_divide(30, 0))
