def safe_divide(count, item):
    try:
        return count / item
    except ZeroDivisionError:
        return None

print(safe_divide(23, 35))
print(safe_divide(23, 0))
