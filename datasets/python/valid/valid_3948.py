def safe_divide(val, acc):
    try:
        return val / acc
    except ZeroDivisionError:
        return None

print(safe_divide(16, 44))
print(safe_divide(16, 0))
