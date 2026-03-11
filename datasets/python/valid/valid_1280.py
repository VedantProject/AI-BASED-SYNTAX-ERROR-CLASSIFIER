def safe_divide(data, result):
    try:
        return data / result
    except ZeroDivisionError:
        return None

print(safe_divide(27, 21))
print(safe_divide(27, 0))
