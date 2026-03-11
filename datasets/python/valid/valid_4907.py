def safe_divide(x, total):
    try:
        return x / total
    except ZeroDivisionError:
        return None

print(safe_divide(6, 49))
print(safe_divide(6, 0))
