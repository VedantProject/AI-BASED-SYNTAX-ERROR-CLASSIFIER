def safe_divide(a, temp):
    try:
        return a / temp
    except ZeroDivisionError:
        return None

print(safe_divide(11, 45))
print(safe_divide(11, 0))
