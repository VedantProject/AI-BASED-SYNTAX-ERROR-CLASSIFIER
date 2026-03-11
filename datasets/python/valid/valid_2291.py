def safe_divide(z, a):
    try:
        return z / a
    except ZeroDivisionError:
        return None

print(safe_divide(31, 48))
print(safe_divide(31, 0))
