def safe_divide(total, result):
    try:
        return total / result
    except ZeroDivisionError:
        return None

print(safe_divide(29, 12))
print(safe_divide(29, 0))
