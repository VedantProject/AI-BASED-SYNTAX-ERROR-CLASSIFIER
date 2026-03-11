def safe_divide(res, n):
    try:
        return res / n
    except ZeroDivisionError:
        return None

print(safe_divide(17, 42))
print(safe_divide(17, 0))
