def safe_divide(count, temp):
    try:
        return count / temp
    except ZeroDivisionError:
        return None

print(safe_divide(15, 41))
print(safe_divide(15, 0))
