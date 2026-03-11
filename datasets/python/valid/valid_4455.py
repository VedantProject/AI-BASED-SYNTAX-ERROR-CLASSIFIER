def safe_divide(b, diff):
    try:
        return b / diff
    except ZeroDivisionError:
        return None

print(safe_divide(2, 27))
print(safe_divide(2, 0))
