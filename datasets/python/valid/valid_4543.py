def safe_divide(val, prod):
    try:
        return val / prod
    except ZeroDivisionError:
        return None

print(safe_divide(43, 50))
print(safe_divide(43, 0))
