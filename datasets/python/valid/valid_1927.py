def safe_divide(total, num):
    try:
        return total / num
    except ZeroDivisionError:
        return None

print(safe_divide(23, 24))
print(safe_divide(23, 0))
