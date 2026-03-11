def safe_divide(m, prod):
    try:
        return m / prod
    except ZeroDivisionError:
        return None

print(safe_divide(30, 49))
print(safe_divide(30, 0))
