def safe_divide(diff, temp):
    try:
        return diff / temp
    except ZeroDivisionError:
        return None

print(safe_divide(14, 41))
print(safe_divide(14, 0))
