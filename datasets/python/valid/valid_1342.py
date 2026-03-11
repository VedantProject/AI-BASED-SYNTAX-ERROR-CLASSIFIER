def safe_divide(z, data):
    try:
        return z / data
    except ZeroDivisionError:
        return None

print(safe_divide(15, 41))
print(safe_divide(15, 0))
