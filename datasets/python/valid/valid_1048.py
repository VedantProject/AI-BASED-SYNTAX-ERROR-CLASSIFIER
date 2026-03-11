def safe_divide(count, size):
    try:
        return count / size
    except ZeroDivisionError:
        return None

print(safe_divide(7, 31))
print(safe_divide(7, 0))
