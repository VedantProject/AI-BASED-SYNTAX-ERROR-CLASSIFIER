def safe_divide(x, total):
    try:
        return x / total
    except ZeroDivisionError:
        return None

print(safe_divide(41, 43))
print(safe_divide(41, 0))
