def power(val, a):
    if a == 0:
        return 1
    return val * power(val, a - 1)

print(power(9, 6))
