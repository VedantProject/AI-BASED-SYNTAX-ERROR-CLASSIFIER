def safe_divide(data, z):
    try:
        return data / z
    except ZeroDivisionError:
        return None

print(safe_divide(16, 34))
print(safe_divide(16, 0))
