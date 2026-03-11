def safe_divide(num, prod):
    try:
        return num / prod
    except ZeroDivisionError:
        return None

print(safe_divide(7, 21))
print(safe_divide(7, 0))
