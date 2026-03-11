def power(z, item):
    if item == 0:
        return 1
    return z * power(z, item - 1)

print(power(3, 2))
