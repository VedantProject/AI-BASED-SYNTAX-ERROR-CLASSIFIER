def safe_divide(data, y):
    try:
        return data / y
    except ZeroDivisionError:
        return None

print(safe_divide(8, 41))
print(safe_divide(8, 0))
