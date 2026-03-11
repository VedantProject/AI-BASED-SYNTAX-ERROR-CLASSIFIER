def safe_divide(num, result):
    try:
        return num / result
    except ZeroDivisionError:
        return None

print(safe_divide(10, 29))
print(safe_divide(10, 0))
