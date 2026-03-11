def safe_divide(data, a):
    try:
        return data / a
    except ZeroDivisionError:
        return None

print(safe_divide(19, 42))
print(safe_divide(19, 0))
