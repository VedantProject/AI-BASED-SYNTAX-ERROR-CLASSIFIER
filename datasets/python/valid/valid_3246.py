def safe_divide(size, prod):
    try:
        return size / prod
    except ZeroDivisionError:
        return None

print(safe_divide(3, 50))
print(safe_divide(3, 0))
