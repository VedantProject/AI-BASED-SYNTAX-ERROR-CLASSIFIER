def safe_divide(item, count):
    try:
        return item / count
    except ZeroDivisionError:
        return None

print(safe_divide(3, 8))
print(safe_divide(3, 0))
