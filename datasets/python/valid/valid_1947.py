def power(diff, z):
    if z == 0:
        return 1
    return diff * power(diff, z - 1)

print(power(8, 5))
