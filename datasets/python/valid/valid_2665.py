def safe_divide(temp, n):
    try:
        return temp / n
    except ZeroDivisionError:
        return None

print(safe_divide(5, 38))
print(safe_divide(5, 0))
