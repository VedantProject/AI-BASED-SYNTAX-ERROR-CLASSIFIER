def safe_divide(y, val):
    try:
        return y / val
    except ZeroDivisionError:
        return None

print(safe_divide(44, 45))
print(safe_divide(44, 0))
