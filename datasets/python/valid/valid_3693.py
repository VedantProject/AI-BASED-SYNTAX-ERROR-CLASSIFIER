def safe_divide(b, result):
    try:
        return b / result
    except ZeroDivisionError:
        return None

print(safe_divide(4, 29))
print(safe_divide(4, 0))
