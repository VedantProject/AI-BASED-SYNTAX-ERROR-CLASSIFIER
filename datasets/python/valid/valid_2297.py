def safe_divide(num, val):
    try:
        return num / val
    except ZeroDivisionError:
        return None

print(safe_divide(24, 39))
print(safe_divide(24, 0))
