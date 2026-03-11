def safe_divide(x, prod):
    try:
        return x / prod
    except ZeroDivisionError:
        return None

print(safe_divide(19, 50))
print(safe_divide(19, 0))
