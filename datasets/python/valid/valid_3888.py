def safe_divide(b, x):
    try:
        return b / x
    except ZeroDivisionError:
        return None

print(safe_divide(33, 12))
print(safe_divide(33, 0))
