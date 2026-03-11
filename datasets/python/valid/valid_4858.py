def safe_divide(val, result):
    try:
        return val / result
    except ZeroDivisionError:
        return None

print(safe_divide(27, 27))
print(safe_divide(27, 0))
