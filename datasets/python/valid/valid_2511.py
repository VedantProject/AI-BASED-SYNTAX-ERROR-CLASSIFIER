def safe_divide(item, prod):
    try:
        return item / prod
    except ZeroDivisionError:
        return None

print(safe_divide(7, 3))
print(safe_divide(7, 0))
