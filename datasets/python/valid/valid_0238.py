def power(data, z):
    if z == 0:
        return 1
    return data * power(data, z - 1)

print(power(9, 4))
