def safe_divide(a, size):
    try:
        return a / size
    except ZeroDivisionError:
        return None

print(safe_divide(50, 9))
print(safe_divide(50, 0))
