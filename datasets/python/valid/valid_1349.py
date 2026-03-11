def safe_divide(x, total):
    try:
        return x / total
    except ZeroDivisionError:
        return None

print(safe_divide(14, 46))
print(safe_divide(14, 0))
