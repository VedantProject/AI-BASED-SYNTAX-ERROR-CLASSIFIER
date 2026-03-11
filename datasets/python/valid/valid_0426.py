def safe_divide(n, result):
    try:
        return n / result
    except ZeroDivisionError:
        return None

print(safe_divide(35, 37))
print(safe_divide(35, 0))
