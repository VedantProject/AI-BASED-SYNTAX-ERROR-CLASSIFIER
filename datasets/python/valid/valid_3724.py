def safe_divide(item, acc):
    try:
        return item / acc
    except ZeroDivisionError:
        return None

print(safe_divide(5, 10))
print(safe_divide(5, 0))
