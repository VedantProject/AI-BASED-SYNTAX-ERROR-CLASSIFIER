def safe_divide(size, prod):
    try:
        return size / prod
    except ZeroDivisionError:
        return None

print(safe_divide(49, 35))
print(safe_divide(49, 0))
