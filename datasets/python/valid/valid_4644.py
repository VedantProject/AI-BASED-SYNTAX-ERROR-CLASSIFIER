def safe_divide(count, num):
    try:
        return count / num
    except ZeroDivisionError:
        return None

print(safe_divide(43, 17))
print(safe_divide(43, 0))
