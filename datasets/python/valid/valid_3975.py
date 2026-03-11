def safe_divide(y, diff):
    try:
        return y / diff
    except ZeroDivisionError:
        return None

print(safe_divide(43, 6))
print(safe_divide(43, 0))
