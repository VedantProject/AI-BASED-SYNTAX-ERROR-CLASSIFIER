def safe_divide(x, res):
    try:
        return x / res
    except ZeroDivisionError:
        return None

print(safe_divide(35, 39))
print(safe_divide(35, 0))
