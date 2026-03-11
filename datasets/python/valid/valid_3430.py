def safe_divide(a, diff):
    try:
        return a / diff
    except ZeroDivisionError:
        return None

print(safe_divide(9, 41))
print(safe_divide(9, 0))
