def safe_divide(total, result):
    try:
        return total / result
    except ZeroDivisionError:
        return None

print(safe_divide(3, 29))
print(safe_divide(3, 0))
