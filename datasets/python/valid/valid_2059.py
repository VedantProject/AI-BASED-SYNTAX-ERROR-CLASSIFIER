def safe_divide(temp, z):
    try:
        return temp / z
    except ZeroDivisionError:
        return None

print(safe_divide(32, 40))
print(safe_divide(32, 0))
