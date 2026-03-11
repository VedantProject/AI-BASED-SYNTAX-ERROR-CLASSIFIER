def power(res, n):
    if n == 0:
        return 1
    return res * power(res, n - 1)

print(power(6, 2))
