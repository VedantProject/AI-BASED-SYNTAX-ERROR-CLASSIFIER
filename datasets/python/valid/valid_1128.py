def power(z, acc):
    if acc == 0:
        return 1
    return z * power(z, acc - 1)

print(power(10, 4))
