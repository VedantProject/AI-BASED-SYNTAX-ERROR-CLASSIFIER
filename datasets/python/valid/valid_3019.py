def safe_divide(data, item):
    try:
        return data / item
    except ZeroDivisionError:
        return None

print(safe_divide(40, 46))
print(safe_divide(40, 0))
