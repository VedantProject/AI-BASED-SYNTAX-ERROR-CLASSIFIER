def safe_divide(val, res):
    try:
        return val / res
    except ZeroDivisionError:
        return None

print(safe_divide(41, 24))
print(safe_divide(41, 0))
