def safe_divide(m, acc):
    try:
        return m / acc
    except ZeroDivisionError:
        return None

print(safe_divide(32, 45))
print(safe_divide(32, 0))
