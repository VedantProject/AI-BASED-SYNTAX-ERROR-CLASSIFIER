def power(res, m):
    if m == 0:
        return 1
    return res * power(res, m - 1)

print(power(3, 3))
