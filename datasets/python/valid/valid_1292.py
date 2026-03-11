def safe_divide(temp, diff):
    try:
        return temp / diff
    except ZeroDivisionError:
        return None

print(safe_divide(3, 15))
print(safe_divide(3, 0))
