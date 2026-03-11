def safe_divide(prod, a):
    try:
        return prod / a
    except ZeroDivisionError:
        return None

print(safe_divide(8, 41))
print(safe_divide(8, 0))
