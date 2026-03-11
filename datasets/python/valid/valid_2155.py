def power(x, val):
    if val == 0:
        return 1
    return x * power(x, val - 1)

print(power(9, 4))
