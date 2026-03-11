def safe_divide(b, temp):
    try:
        return b / temp
    except ZeroDivisionError:
        return None

print(safe_divide(48, 28))
print(safe_divide(48, 0))
