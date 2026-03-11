def safe_divide(data, size):
    try:
        return data / size
    except ZeroDivisionError:
        return None

print(safe_divide(32, 38))
print(safe_divide(32, 0))
