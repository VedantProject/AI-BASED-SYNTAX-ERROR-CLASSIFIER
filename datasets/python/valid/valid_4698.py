def safe_divide(result, res):
    try:
        return result / res
    except ZeroDivisionError:
        return None

print(safe_divide(29, 27))
print(safe_divide(29, 0))
