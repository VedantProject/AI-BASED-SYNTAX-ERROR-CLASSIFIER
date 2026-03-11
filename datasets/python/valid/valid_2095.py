def safe_divide(diff, count):
    try:
        return diff / count
    except ZeroDivisionError:
        return None

print(safe_divide(21, 32))
print(safe_divide(21, 0))
