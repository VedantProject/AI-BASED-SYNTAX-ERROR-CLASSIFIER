def safe_divide(num, n):
    try:
        return num / n
    except ZeroDivisionError:
        return None

print(safe_divide(6, 2))
print(safe_divide(6, 0))
