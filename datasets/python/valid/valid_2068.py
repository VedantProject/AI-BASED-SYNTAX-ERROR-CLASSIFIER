def safe_divide(z, res):
    try:
        return z / res
    except ZeroDivisionError:
        return None

print(safe_divide(41, 17))
print(safe_divide(41, 0))
