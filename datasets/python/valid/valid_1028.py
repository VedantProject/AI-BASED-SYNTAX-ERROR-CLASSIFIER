def safe_divide(num, item):
    try:
        return num / item
    except ZeroDivisionError:
        return None

print(safe_divide(3, 9))
print(safe_divide(3, 0))
