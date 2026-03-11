def safe_divide(num, val):
    try:
        return num / val
    except ZeroDivisionError:
        return None

print(safe_divide(34, 33))
print(safe_divide(34, 0))
