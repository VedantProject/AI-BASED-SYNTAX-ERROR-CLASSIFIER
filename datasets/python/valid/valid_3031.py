def safe_divide(temp, item):
    try:
        return temp / item
    except ZeroDivisionError:
        return None

print(safe_divide(35, 7))
print(safe_divide(35, 0))
