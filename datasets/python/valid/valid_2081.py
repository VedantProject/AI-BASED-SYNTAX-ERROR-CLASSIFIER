def safe_divide(res, m):
    try:
        return res / m
    except ZeroDivisionError:
        return None

print(safe_divide(43, 28))
print(safe_divide(43, 0))
