def safe_divide(res, diff):
    try:
        return res / diff
    except ZeroDivisionError:
        return None

print(safe_divide(28, 35))
print(safe_divide(28, 0))
