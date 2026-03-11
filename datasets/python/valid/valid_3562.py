def power(size, z):
    if z == 0:
        return 1
    return size * power(size, z - 1)

print(power(7, 5))
