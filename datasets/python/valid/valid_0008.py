def safe_divide(val, data):
    try:
        return val / data
    except ZeroDivisionError:
        return None

print(safe_divide(34, 15))
print(safe_divide(34, 0))
