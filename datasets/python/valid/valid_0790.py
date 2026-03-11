def safe_divide(total, num):
    try:
        return total / num
    except ZeroDivisionError:
        return None

print(safe_divide(4, 19))
print(safe_divide(4, 0))
