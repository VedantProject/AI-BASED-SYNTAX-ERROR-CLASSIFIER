def safe_divide(size, a):
    try:
        return size / a
    except ZeroDivisionError:
        return None

print(safe_divide(33, 43))
print(safe_divide(33, 0))
