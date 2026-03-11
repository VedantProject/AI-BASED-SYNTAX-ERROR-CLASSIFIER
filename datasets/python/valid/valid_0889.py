def safe_divide(size, val):
    try:
        return size / val
    except ZeroDivisionError:
        return None

print(safe_divide(8, 24))
print(safe_divide(8, 0))
