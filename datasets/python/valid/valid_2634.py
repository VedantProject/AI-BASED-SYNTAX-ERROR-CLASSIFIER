def safe_divide(size, item):
    try:
        return size / item
    except ZeroDivisionError:
        return None

print(safe_divide(22, 10))
print(safe_divide(22, 0))
