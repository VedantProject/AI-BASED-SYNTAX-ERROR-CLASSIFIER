def safe_divide(b, res):
    try:
        return b / res
    except ZeroDivisionError:
        return None

print(safe_divide(50, 4))
print(safe_divide(50, 0))
