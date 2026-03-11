def power(a, z):
    if z == 0:
        return 1
    return a * power(a, z - 1)

print(power(10, 2))
