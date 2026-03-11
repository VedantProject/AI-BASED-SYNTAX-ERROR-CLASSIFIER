def safe_divide(data, temp):
    try:
        return data / temp
    except ZeroDivisionError:
        return None

print(safe_divide(8, 38))
print(safe_divide(8, 0))
