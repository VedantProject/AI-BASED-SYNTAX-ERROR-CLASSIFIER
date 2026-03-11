def safe_divide(result, item):
    try:
        return result / item
    except ZeroDivisionError:
        return None

print(safe_divide(14, 46))
print(safe_divide(14, 0))
