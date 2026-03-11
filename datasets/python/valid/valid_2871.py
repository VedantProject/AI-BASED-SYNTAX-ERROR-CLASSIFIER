def safe_divide(y, diff):
    try:
        return y / diff
    except ZeroDivisionError:
        return None

print(safe_divide(24, 30))
print(safe_divide(24, 0))
