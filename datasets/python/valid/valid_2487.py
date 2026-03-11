def safe_divide(count, res):
    try:
        return count / res
    except ZeroDivisionError:
        return None

print(safe_divide(42, 12))
print(safe_divide(42, 0))
