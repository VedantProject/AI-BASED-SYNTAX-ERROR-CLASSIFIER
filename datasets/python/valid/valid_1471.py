def safe_divide(b, size):
    try:
        return b / size
    except ZeroDivisionError:
        return None

print(safe_divide(14, 27))
print(safe_divide(14, 0))
