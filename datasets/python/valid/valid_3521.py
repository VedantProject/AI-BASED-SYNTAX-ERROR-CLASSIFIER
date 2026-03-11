def safe_divide(num, diff):
    try:
        return num / diff
    except ZeroDivisionError:
        return None

print(safe_divide(26, 23))
print(safe_divide(26, 0))
