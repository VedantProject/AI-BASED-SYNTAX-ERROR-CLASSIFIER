def safe_divide(res, count):
    try:
        return res / count
    except ZeroDivisionError:
        return None

print(safe_divide(18, 25))
print(safe_divide(18, 0))
