def power(y, x):
    if x == 0:
        return 1
    return y * power(y, x - 1)

print(power(3, 4))
