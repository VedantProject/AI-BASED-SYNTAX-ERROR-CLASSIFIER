def safe_divide(result, data):
    try:
        return result / data
    except ZeroDivisionError:
        return None

print(safe_divide(39, 13))
print(safe_divide(39, 0))
