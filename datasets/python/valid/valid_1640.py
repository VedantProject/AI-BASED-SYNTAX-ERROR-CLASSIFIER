def safe_divide(acc, result):
    try:
        return acc / result
    except ZeroDivisionError:
        return None

print(safe_divide(13, 48))
print(safe_divide(13, 0))
