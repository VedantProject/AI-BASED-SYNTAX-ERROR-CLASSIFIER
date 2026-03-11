def safe_divide(y, a):
    try:
        return y / a
    except ZeroDivisionError:
        return None

print(safe_divide(13, 16))
print(safe_divide(13, 0))
