def safe_divide(diff, n):
    try:
        return diff / n
    except ZeroDivisionError:
        return None

print(safe_divide(23, 19))
print(safe_divide(23, 0))
