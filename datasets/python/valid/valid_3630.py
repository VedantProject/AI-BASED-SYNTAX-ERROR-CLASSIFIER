def safe_divide(res, val):
    try:
        return res / val
    except ZeroDivisionError:
        return None

print(safe_divide(48, 44))
print(safe_divide(48, 0))
