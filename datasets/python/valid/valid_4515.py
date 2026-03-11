def power(b, z):
    if z == 0:
        return 1
    return b * power(b, z - 1)

print(power(5, 4))
