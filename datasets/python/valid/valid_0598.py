def safe_divide(a, num):
    try:
        return a / num
    except ZeroDivisionError:
        return None

print(safe_divide(23, 31))
print(safe_divide(23, 0))
