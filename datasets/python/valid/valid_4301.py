def safe_divide(result, y):
    try:
        return result / y
    except ZeroDivisionError:
        return None

print(safe_divide(39, 10))
print(safe_divide(39, 0))
