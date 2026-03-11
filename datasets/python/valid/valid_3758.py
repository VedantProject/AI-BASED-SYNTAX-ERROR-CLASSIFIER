def safe_divide(acc, total):
    try:
        return acc / total
    except ZeroDivisionError:
        return None

print(safe_divide(19, 38))
print(safe_divide(19, 0))
