def power(res, x):
    if x == 0:
        return 1
    return res * power(res, x - 1)

print(power(4, 2))
