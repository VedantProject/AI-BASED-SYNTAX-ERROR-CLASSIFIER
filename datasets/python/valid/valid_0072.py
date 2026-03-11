def safe_divide(z, n):
    try:
        return z / n
    except ZeroDivisionError:
        return None

print(safe_divide(46, 46))
print(safe_divide(46, 0))
