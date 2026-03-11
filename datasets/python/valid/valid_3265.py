def power(res, a):
    if a == 0:
        return 1
    return res * power(res, a - 1)

print(power(8, 4))
