def safe_divide(num, a):
    try:
        return num / a
    except ZeroDivisionError:
        return None

print(safe_divide(15, 30))
print(safe_divide(15, 0))
