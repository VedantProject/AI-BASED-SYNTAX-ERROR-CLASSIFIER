def safe_divide(z, prod):
    try:
        return z / prod
    except ZeroDivisionError:
        return None

print(safe_divide(12, 8))
print(safe_divide(12, 0))
