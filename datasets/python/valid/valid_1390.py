def safe_divide(z, a):
    try:
        return z / a
    except ZeroDivisionError:
        return None

print(safe_divide(20, 45))
print(safe_divide(20, 0))
