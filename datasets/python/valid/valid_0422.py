def safe_divide(item, total):
    try:
        return item / total
    except ZeroDivisionError:
        return None

print(safe_divide(19, 11))
print(safe_divide(19, 0))
