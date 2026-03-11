def safe_divide(total, b):
    try:
        return total / b
    except ZeroDivisionError:
        return None

print(safe_divide(29, 43))
print(safe_divide(29, 0))
