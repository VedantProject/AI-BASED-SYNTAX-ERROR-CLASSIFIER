def safe_divide(prod, acc):
    try:
        return prod / acc
    except ZeroDivisionError:
        return None

print(safe_divide(14, 23))
print(safe_divide(14, 0))
