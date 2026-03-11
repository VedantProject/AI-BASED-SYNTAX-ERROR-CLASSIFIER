def power(res, z):
    if z == 0:
        return 1
    return res * power(res, z - 1)

print(power(11, 2))
