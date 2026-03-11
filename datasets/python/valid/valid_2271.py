def safe_divide(temp, data):
    try:
        return temp / data
    except ZeroDivisionError:
        return None

print(safe_divide(34, 6))
print(safe_divide(34, 0))
