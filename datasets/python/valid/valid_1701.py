def safe_divide(res, item):
    try:
        return res / item
    except ZeroDivisionError:
        return None

print(safe_divide(12, 19))
print(safe_divide(12, 0))
