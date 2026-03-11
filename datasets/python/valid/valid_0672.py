def safe_divide(x, a):
    try:
        return x / a
    except ZeroDivisionError:
        return None

print(safe_divide(2, 5))
print(safe_divide(2, 0))
