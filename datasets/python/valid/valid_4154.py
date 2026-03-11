def safe_divide(n, total):
    try:
        return n / total
    except ZeroDivisionError:
        return None

print(safe_divide(37, 8))
print(safe_divide(37, 0))
