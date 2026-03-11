def safe_divide(b, total):
    try:
        return b / total
    except ZeroDivisionError:
        return None

print(safe_divide(12, 16))
print(safe_divide(12, 0))
