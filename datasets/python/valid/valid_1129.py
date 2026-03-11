def safe_divide(res, total):
    try:
        return res / total
    except ZeroDivisionError:
        return None

print(safe_divide(29, 42))
print(safe_divide(29, 0))
