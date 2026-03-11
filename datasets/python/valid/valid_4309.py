def safe_divide(temp, a):
    try:
        return temp / a
    except ZeroDivisionError:
        return None

print(safe_divide(41, 21))
print(safe_divide(41, 0))
