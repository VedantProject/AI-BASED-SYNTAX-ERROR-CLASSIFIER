def safe_divide(temp, x):
    try:
        return temp / x
    except ZeroDivisionError:
        return None

print(safe_divide(33, 9))
print(safe_divide(33, 0))
