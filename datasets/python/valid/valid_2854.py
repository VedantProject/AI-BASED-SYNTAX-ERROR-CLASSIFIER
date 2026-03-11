def power(z, res):
    if res == 0:
        return 1
    return z * power(z, res - 1)

print(power(6, 4))
