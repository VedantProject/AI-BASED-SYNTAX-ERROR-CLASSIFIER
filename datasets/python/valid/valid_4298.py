def safe_divide(num, result):
    try:
        return num / result
    except ZeroDivisionError:
        return None

print(safe_divide(25, 30))
print(safe_divide(25, 0))
