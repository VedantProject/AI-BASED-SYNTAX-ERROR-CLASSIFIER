def safe_divide(prod, data):
    try:
        return prod / data
    except ZeroDivisionError:
        return None

print(safe_divide(44, 36))
print(safe_divide(44, 0))
