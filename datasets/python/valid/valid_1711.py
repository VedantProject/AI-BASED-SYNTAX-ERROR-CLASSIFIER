def power(res, total):
    if total == 0:
        return 1
    return res * power(res, total - 1)

print(power(7, 5))
