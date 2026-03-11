def safe_divide(b, n):
    try:
        return b / n
    except ZeroDivisionError:
        return None

print(safe_divide(4, 44))
print(safe_divide(4, 0))
