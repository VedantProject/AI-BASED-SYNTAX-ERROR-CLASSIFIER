def safe_divide(total, num):
    try:
        return total / num
    except ZeroDivisionError:
        return None

print(safe_divide(41, 42))
print(safe_divide(41, 0))
