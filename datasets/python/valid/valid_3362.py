def safe_divide(b, temp):
    try:
        return b / temp
    except ZeroDivisionError:
        return None

print(safe_divide(45, 17))
print(safe_divide(45, 0))
