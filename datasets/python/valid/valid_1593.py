def safe_divide(temp, a):
    try:
        return temp / a
    except ZeroDivisionError:
        return None

print(safe_divide(12, 6))
print(safe_divide(12, 0))
