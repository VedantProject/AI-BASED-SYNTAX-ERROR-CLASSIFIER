def safe_divide(acc, count):
    try:
        return acc / count
    except ZeroDivisionError:
        return None

print(safe_divide(3, 40))
print(safe_divide(3, 0))
