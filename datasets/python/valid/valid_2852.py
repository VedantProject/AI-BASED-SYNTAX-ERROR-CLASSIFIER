def safe_divide(y, x):
    try:
        return y / x
    except ZeroDivisionError:
        return None

print(safe_divide(15, 5))
print(safe_divide(15, 0))
