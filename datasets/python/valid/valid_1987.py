def safe_divide(res, b):
    try:
        return res / b
    except ZeroDivisionError:
        return None

print(safe_divide(19, 19))
print(safe_divide(19, 0))
