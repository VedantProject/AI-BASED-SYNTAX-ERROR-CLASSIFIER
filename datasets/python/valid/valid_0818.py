def safe_divide(res, diff):
    try:
        return res / diff
    except ZeroDivisionError:
        return None

print(safe_divide(38, 27))
print(safe_divide(38, 0))
