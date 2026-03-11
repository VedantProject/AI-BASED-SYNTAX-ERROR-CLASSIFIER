def safe_divide(x, diff):
    try:
        return x / diff
    except ZeroDivisionError:
        return None

print(safe_divide(25, 3))
print(safe_divide(25, 0))
