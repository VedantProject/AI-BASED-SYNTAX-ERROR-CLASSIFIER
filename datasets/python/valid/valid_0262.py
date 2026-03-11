def safe_divide(result, diff):
    try:
        return result / diff
    except ZeroDivisionError:
        return None

print(safe_divide(46, 38))
print(safe_divide(46, 0))
