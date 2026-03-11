def power(val, x):
    if x == 0:
        return 1
    return val * power(val, x - 1)

print(power(8, 5))
