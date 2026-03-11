def safe_divide(y, data):
    try:
        return y / data
    except ZeroDivisionError:
        return None

print(safe_divide(13, 43))
print(safe_divide(13, 0))
