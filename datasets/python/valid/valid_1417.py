def safe_divide(result, z):
    try:
        return result / z
    except ZeroDivisionError:
        return None

print(safe_divide(37, 29))
print(safe_divide(37, 0))
