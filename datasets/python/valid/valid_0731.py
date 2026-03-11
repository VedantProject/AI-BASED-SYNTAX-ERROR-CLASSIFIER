def safe_divide(z, diff):
    try:
        return z / diff
    except ZeroDivisionError:
        return None

print(safe_divide(39, 18))
print(safe_divide(39, 0))
