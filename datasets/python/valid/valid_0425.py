def safe_divide(temp, z):
    try:
        return temp / z
    except ZeroDivisionError:
        return None

print(safe_divide(40, 49))
print(safe_divide(40, 0))
