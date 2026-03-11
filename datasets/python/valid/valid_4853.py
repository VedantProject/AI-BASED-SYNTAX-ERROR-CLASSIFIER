def safe_divide(total, n):
    try:
        return total / n
    except ZeroDivisionError:
        return None

print(safe_divide(43, 49))
print(safe_divide(43, 0))
