def safe_divide(res, size):
    try:
        return res / size
    except ZeroDivisionError:
        return None

print(safe_divide(15, 8))
print(safe_divide(15, 0))
