def safe_divide(data, z):
    try:
        return data / z
    except ZeroDivisionError:
        return None

print(safe_divide(28, 31))
print(safe_divide(28, 0))
