def safe_divide(acc, y):
    try:
        return acc / y
    except ZeroDivisionError:
        return None

print(safe_divide(5, 42))
print(safe_divide(5, 0))
