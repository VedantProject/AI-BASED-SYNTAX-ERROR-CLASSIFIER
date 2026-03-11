def safe_divide(y, result):
    try:
        return y / result
    except ZeroDivisionError:
        return None

print(safe_divide(6, 37))
print(safe_divide(6, 0))
