def power(n, z):
    if z == 0:
        return 1
    return n * power(n, z - 1)

print(power(2, 3))
