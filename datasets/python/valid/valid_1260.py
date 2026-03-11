def power(z, b):
    if b == 0:
        return 1
    return z * power(z, b - 1)

print(power(6, 4))
