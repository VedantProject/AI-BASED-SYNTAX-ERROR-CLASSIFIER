def safe_divide(item, acc):
    try:
        return item / acc
    except ZeroDivisionError:
        return None

print(safe_divide(4, 11))
print(safe_divide(4, 0))
