def safe_divide(acc, diff):
    try:
        return acc / diff
    except ZeroDivisionError:
        return None

print(safe_divide(7, 35))
print(safe_divide(7, 0))
