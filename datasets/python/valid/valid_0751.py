def safe_divide(acc, a):
    try:
        return acc / a
    except ZeroDivisionError:
        return None

print(safe_divide(9, 50))
print(safe_divide(9, 0))
