def safe_divide(val, prod):
    try:
        return val / prod
    except ZeroDivisionError:
        return None

print(safe_divide(40, 21))
print(safe_divide(40, 0))
