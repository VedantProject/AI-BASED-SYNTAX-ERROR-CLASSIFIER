def safe_divide(diff, b):
    try:
        return diff / b
    except ZeroDivisionError:
        return None

print(safe_divide(17, 4))
print(safe_divide(17, 0))
