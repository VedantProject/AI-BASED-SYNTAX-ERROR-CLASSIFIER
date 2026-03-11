def safe_divide(x, total):
    try:
        return x / total
    except ZeroDivisionError:
        return None

print(safe_divide(34, 10))
print(safe_divide(34, 0))
