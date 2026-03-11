def safe_divide(count, total):
    try:
        return count / total
    except ZeroDivisionError:
        return None

print(safe_divide(7, 3))
print(safe_divide(7, 0))
