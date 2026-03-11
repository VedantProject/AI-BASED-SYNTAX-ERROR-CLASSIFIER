def power(z, y):
    if y == 0:
        return 1
    return z * power(z, y - 1)

print(power(7, 2))
