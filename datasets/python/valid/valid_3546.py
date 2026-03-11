def safe_divide(item, a):
    try:
        return item / a
    except ZeroDivisionError:
        return None

print(safe_divide(16, 16))
print(safe_divide(16, 0))
